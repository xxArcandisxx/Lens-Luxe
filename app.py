from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os
from datetime import datetime, timedelta
import secrets
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# File Upload Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'profiles')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Email Configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', True)
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = ('Lens&Luxe', 'noreply@lensandluxe.com')

db = SQLAlchemy(app)
mail = Mail(app)

# ===========================
# DATABASE MODELS
# ===========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), default='')
    interests = db.Column(db.String(500), default='')  # Comma-separated interests
    newsletter = db.Column(db.Boolean, default=True)
    profile_picture = db.Column(db.String(255), default='')
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def generate_reset_token(self):
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        return self.reset_token
    
    def verify_reset_token(self, token):
        if self.reset_token != token:
            return False
        if self.reset_token_expiry < datetime.utcnow():
            return False
        return True
    
    def clear_reset_token(self):
        self.reset_token = None
        self.reset_token_expiry = None

# ===========================
# LOGIN REQUIRED DECORATOR
# ===========================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ===========================
# HELPER FUNCTIONS
# ===========================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_profile_picture(file):
    """Save uploaded profile picture and return filename"""
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = f"{session['user_id']}_{secrets.token_hex(4)}.{file.filename.rsplit('.', 1)[1].lower()}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filename
    return None

def send_reset_email(user, reset_token):
    """Send password reset email"""
    reset_url = url_for('reset_password', token=reset_token, _external=True)
    msg = Message(
        'Password Reset Request - Lens&Luxe',
        recipients=[user.email],
        html=f'''
        <h2>Password Reset Request</h2>
        <p>Dear {user.first_name},</p>
        <p>We received a request to reset your password. Click the link below to reset it:</p>
        <a href="{reset_url}" style="padding: 10px 20px; background-color: #5a1020; color: white; text-decoration: none; border-radius: 5px; display: inline-block;">
            Reset Password
        </a>
        <p style="margin-top: 20px;">This link expires in 1 hour.</p>
        <p>If you didn't request this, please ignore this email.</p>
        <p>Best regards,<br>Lens&Luxe Team</p>
        '''
    )
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# ===========================
# ROUTES
# ===========================

@app.route('/')
def home():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('index.html', user=user)

@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        # Handle account creation
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        phone = request.form.get('phone', '')
        interests = ','.join(request.form.getlist('interests'))
        newsletter = 'newsletter' in request.form

        # Validation
        if not all([first_name, last_name, email, password]):
            return jsonify({'error': 'Please fill in all required fields'}), 400

        if len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters long'}), 400

        if password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400

        # Create new user
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            interests=interests,
            newsletter=newsletter
        )
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()

            # Log user in automatically after registration
            session['user_id'] = new_user.id
            session['user_name'] = first_name

            return jsonify({'success': True, 'message': f'Welcome {first_name}! Account created successfully.'}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error creating account. Please try again.'}), 500

    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('account.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return jsonify({'error': 'Please enter email and password'}), 400

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.first_name
            return jsonify({'success': True, 'message': f'Welcome back, {user.first_name}!'}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])

    return render_template('login.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile edit page"""
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        try:
            # Update basic user info
            user.first_name = request.form.get('firstName', user.first_name)
            user.last_name = request.form.get('lastName', user.last_name)
            user.phone = request.form.get('phone', user.phone)
            user.newsletter = 'newsletter' in request.form
            user.interests = ','.join(request.form.getlist('interests'))
            
            # Check if new email is provided and is different from current
            new_email = request.form.get('email', user.email)
            if new_email != user.email:
                # Check if email already exists
                existing_user = User.query.filter_by(email=new_email).first()
                if existing_user:
                    return jsonify({'error': 'Email already registered'}), 400
                user.email = new_email
            
            # Handle profile picture upload
            if 'profilePicture' in request.files:
                file = request.files['profilePicture']
                if file and file.filename:
                    # Delete old profile picture if exists
                    if user.profile_picture:
                        old_path = os.path.join(app.config['UPLOAD_FOLDER'], user.profile_picture)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    
                    # Save new profile picture
                    filename = save_profile_picture(file)
                    if filename:
                        user.profile_picture = filename
                    else:
                        return jsonify({'error': 'Invalid file type. Only JPG, PNG, GIF allowed.'}), 400
            
            db.session.commit()
            return jsonify({'success': True, 'message': 'Profile updated successfully!'}), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error updating profile: {str(e)}'}), 500
    
    return render_template('edit_profile.html', user=user)

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    if request.method == 'POST':
        user = User.query.get(session['user_id'])
        current_password = request.form.get('currentPassword')
        new_password = request.form.get('newPassword')
        confirm_password = request.form.get('confirmPassword')
        
        # Validate current password
        if not user.check_password(current_password):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Validate new password
        if not new_password or len(new_password) < 8:
            return jsonify({'error': 'New password must be at least 8 characters long'}), 400
        
        if new_password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), 400
        
        if current_password == new_password:
            return jsonify({'error': 'New password must be different from current password'}), 400
        
        # Update password
        try:
            user.set_password(new_password)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Password changed successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error changing password'}), 500
    
    return render_template('change_password.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Request password reset"""
    if request.method == 'POST':
        email = request.form.get('email')
        
        if not email:
            return jsonify({'error': 'Please enter your email'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # For security, don't reveal if email exists
            return jsonify({'success': True, 'message': 'If an account exists with this email, a reset link has been sent.'}), 200
        
        try:
            # Generate reset token
            reset_token = user.generate_reset_token()
            db.session.commit()
            
            # Send reset email
            if send_reset_email(user, reset_token):
                return jsonify({'success': True, 'message': 'Password reset link sent to your email!'}), 200
            else:
                return jsonify({'error': 'Error sending reset email. Please try again.'}), 500
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error processing request'}), 500
    
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password using token"""
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.verify_reset_token(token):
        return render_template('reset_password.html', valid_token=False, user=None)
    
    if request.method == 'POST':
        new_password = request.form.get('newPassword')
        confirm_password = request.form.get('confirmPassword')
        
        # Validate
        if not new_password or len(new_password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters long'}), 400
        
        if new_password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), 400
        
        try:
            user.set_password(new_password)
            user.clear_reset_token()
            db.session.commit()
            return jsonify({'success': True, 'message': 'Password reset successfully! Redirecting to login...'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error resetting password'}), 500
    
    return render_template('reset_password.html', valid_token=True, token=token, user=user)

@app.route('/api/user-status')
def user_status():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return jsonify({
            'logged_in': True,
            'user_name': user.first_name,
            'email': user.email
        })
    return jsonify({'logged_in': False})

# ===========================
# ERROR HANDLERS
# ===========================
@app.errorhandler(404)
def not_found(error):
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('404.html', user=user), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
