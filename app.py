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
import urllib.request
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
# Setup database connection
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # SQLAlchemy 1.4+ requires 'postgresql://' instead of 'postgres://'
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
elif os.environ.get('VERCEL') == '1':
    # Fallback for Vercel testing without external DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/users.db'
else:
    # Fallback for local development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

# File Upload Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'profiles')
POST_UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'posts')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB

try:
    Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
    Path(POST_UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
except OSError:
    print("Could not create upload folders. This is normal on read-only environments like Vercel.")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['POST_UPLOAD_FOLDER'] = POST_UPLOAD_FOLDER
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
    bio = db.Column(db.String(500), default='')
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='author', lazy=True, cascade="all, delete-orphan")
    tip_votes = db.relationship('TipVote', backref='user', lazy=True, cascade="all, delete-orphan")

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

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(500), default='')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TipVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tip_id = db.Column(db.Integer, db.ForeignKey('tip.id'), nullable=False)
    vote_type = db.Column(db.String(10), nullable=False)  # 'like' or 'dislike'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'tip_id', name='unique_user_tip_vote'),)

class Tip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'fashion' or 'photography'
    tags = db.Column(db.String(500), default='')
    image = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author = db.relationship('User', backref='tips')
    votes = db.relationship('TipVote', backref='tip', lazy=True, cascade="all, delete-orphan")

# ===========================
# LOGIN REQUIRED DECORATOR
# ===========================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        # Prevent 500 errors if user session exists but database is empty 
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ===========================
# HELPER FUNCTIONS
# ===========================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_vercel_blob(filename, file_content):
    token = os.environ.get('BLOB_READ_WRITE_TOKEN')
    if not token:
        print("BLOB_READ_WRITE_TOKEN not found! Falling back to local save if configured.")
        return None
        
    url = f"https://blob.vercel-storage.com/{filename}"
    req = urllib.request.Request(url, data=file_content, method='PUT')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('x-api-version', '7')
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            return result.get('url')
    except Exception as e:
        print(f"Blob upload failed: {e}")
        return None

def save_profile_picture(file):
    """Save uploaded profile picture and return filename or URL"""
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = f"profiles_{session['user_id']}_{secrets.token_hex(4)}.{file.filename.rsplit('.', 1)[1].lower()}"
        
        # Try Vercel Blob first
        file_content = file.read()
        blob_url = upload_to_vercel_blob(filename, file_content)
        if blob_url:
            return blob_url
            
        # Fallback to local file save
        file.seek(0) # Reset stream
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filename
    return None

def save_post_picture(file):
    """Save uploaded post picture and return filename or URL"""
    if file and allowed_file(file.filename):
        filename = f"post_{session['user_id']}_{secrets.token_hex(6)}.{file.filename.rsplit('.', 1)[1].lower()}"
        
        # Try Vercel Blob first
        file_content = file.read()
        blob_url = upload_to_vercel_blob(filename, file_content)
        if blob_url:
            return blob_url
            
        # Fallback to local save
        file.seek(0)
        filepath = os.path.join(app.config['POST_UPLOAD_FOLDER'], filename)
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
        if email: email = email.lower()
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
            session.permanent = True
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
        if email: email = email.lower()
        password = request.form.get('password')

        if not email or not password:
            return jsonify({'error': 'Please enter email and password'}), 400

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session.permanent = True
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

@app.route('/settings')
@login_required
def settings():
    user = User.query.get(session['user_id'])
    return render_template('settings.html', user=user)

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
            user.bio = request.form.get('bio', user.bio)
            user.newsletter = 'newsletter' in request.form
            user.interests = ','.join(request.form.getlist('interests'))
            
            # Check if new email is provided and is different from current
            new_email = request.form.get('email', user.email)
            if new_email: new_email = new_email.lower()
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
        if email: email = email.lower()
        
        if not email:
            return jsonify({'error': 'Please enter your email'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({'error': "Account doesn't exist."}), 400
        
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
# ===========================
# BLOG ROUTES
# ===========================

@app.route('/api/upload_image', methods=['POST'])
@login_required
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    file = request.files['image']
    if file and file.filename:
        filename = save_post_picture(file)
        if filename:
            if filename.startswith('http'):
                return jsonify({'url': filename}), 200
            else:
                return jsonify({'url': url_for('static', filename='uploads/posts/' + filename)}), 200
    return jsonify({'error': 'Failed to upload image'}), 500

@app.route('/blog')
def blog():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    user = User.query.get(session['user_id']) if 'user_id' in session else None
    return render_template('blog.html', posts=posts, user=user)

@app.route('/blog/create', methods=['GET', 'POST'])
@login_required
def blog_create():
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.get('tags', '')
        
        if not title or not content:
            return jsonify({'error': 'Title and content are required'}), 400
            
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                image_filename = save_post_picture(file)
                if not image_filename:
                    return jsonify({'error': 'Invalid image file type'}), 400
        
        post = Post(title=title, content=content, image=image_filename, tags=tags, user_id=user.id)
        try:
            db.session.add(post)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Post created successfully!', 'redirect': url_for('blog')}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to create post'}), 500
            
    return render_template('blog_create.html', user=user)

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get(session['user_id']) if 'user_id' in session else None
    return render_template('blog_post.html', post=post, user=user)

@app.route('/blog/<int:post_id>/comment', methods=['POST'])
@login_required
def blog_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content')
    if not content:
        return redirect(url_for('blog_post', post_id=post.id))
        
    comment = Comment(content=content, user_id=session['user_id'], post_id=post.id)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('blog_post', post_id=post.id))

@app.route('/blog/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def blog_edit(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get(session['user_id'])
    if post.user_id != user.id:
        return redirect(url_for('blog'))
        
    if request.method == 'POST':
        post.title = request.form.get('title', post.title)
        post.content = request.form.get('content', post.content)
        post.tags = request.form.get('tags', post.tags)
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                if post.image and not ',' in post.image:
                    old_path = os.path.join(app.config['POST_UPLOAD_FOLDER'], post.image)
                    if not post.image.startswith('http') and os.path.exists(old_path):
                        os.remove(old_path)
                image_filename = save_post_picture(file)
                if image_filename:
                    post.image = image_filename
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Post updated!', 'redirect': url_for('blog_post', post_id=post.id)}), 200
        
    return render_template('blog_edit.html', post=post, user=user)

@app.route('/blog/<int:post_id>/delete', methods=['POST'])
@login_required
def blog_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if post.image:
        for img in post.image.split(','):
            img = img.strip()
            if img:
                old_path = os.path.join(app.config['POST_UPLOAD_FOLDER'], img)
                if not img.startswith('http') and os.path.exists(old_path):
                    os.remove(old_path)
            
    db.session.delete(post)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Post deleted', 'redirect': url_for('blog')}), 200

@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def comment_delete(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
        
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Comment deleted', 'redirect': url_for('blog_post', post_id=post_id)}), 200

@app.route('/api/debug-db')
def debug_db():
    uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    return jsonify({
        'using_neon_postgres': 'postgres' in uri or 'neon.tech' in uri,
        'using_temporary_db': '/tmp/' in uri,
        'is_vercel_environment': os.environ.get('VERCEL') == '1'
    })

# ===========================
# TIPS ROUTES
# ===========================

@app.route('/tips')
def tips():
    category = request.args.get('category', None)
    if category:
        tips_list = Tip.query.filter_by(category=category).order_by(Tip.created_at.desc()).all()
    else:
        tips_list = Tip.query.order_by(Tip.created_at.desc()).all()

    user = User.query.get(session['user_id']) if 'user_id' in session else None

    # Try to load subtitle for each tip
    try:
        from sqlalchemy import text
        for tip in tips_list:
            try:
                result = db.session.execute(text("SELECT subtitle FROM tip WHERE id = :id"), {"id": tip.id}).first()
                tip.subtitle = result[0] if result and result[0] else (tip.content[:150] + '...')
            except:
                tip.subtitle = tip.content[:150] + '...'
    except:
        # If subtitle column doesn't exist, use content excerpt
        for tip in tips_list:
            tip.subtitle = tip.content[:150] + '...'

    # Add vote counts to each tip
    for tip in tips_list:
        tip.like_count = len([v for v in tip.votes if v.vote_type == 'like'])
        tip.dislike_count = len([v for v in tip.votes if v.vote_type == 'dislike'])
        tip.user_vote = None
        if user:
            user_vote = next((v for v in tip.votes if v.user_id == user.id), None)
            if user_vote:
                tip.user_vote = user_vote.vote_type

    return render_template('tips.html', tips=tips_list, user=user, category=category)

@app.route('/tips/create', methods=['GET', 'POST'])
@login_required
def tips_create():
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        title = request.form.get('title')
        subtitle = request.form.get('subtitle', '')
        content = request.form.get('content')
        category = request.form.get('category')
        tags = request.form.get('tags', '')

        if not title or not content or not category:
            return jsonify({'error': 'Title, content, and category are required'}), 400

        if not subtitle:
            return jsonify({'error': 'Subtitle is required'}), 400

        if not tags or not tags.strip():
            return jsonify({'error': 'Tags are required'}), 400

        if category not in ['fashion', 'photography']:
            return jsonify({'error': 'Invalid category'}), 400

        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                image_filename = save_post_picture(file)
                if not image_filename:
                    return jsonify({'error': 'Invalid image file type'}), 400

        tip = Tip(title=title, content=content, category=category, tags=tags.strip(), image=image_filename, user_id=user.id)

        try:
            db.session.add(tip)
            db.session.flush()  # Get the ID without committing

            # Try to set subtitle if column exists
            try:
                from sqlalchemy import text
                db.session.execute(text(f"UPDATE tip SET subtitle = :subtitle WHERE id = :id"),
                                 {"subtitle": subtitle, "id": tip.id})
            except:
                pass  # Column might not exist yet

            db.session.commit()
            return jsonify({'success': True, 'message': 'Tip published successfully!', 'redirect': url_for('tips')}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to publish tip'}), 500

    return render_template('tips_create.html', user=user)

@app.route('/tips/<int:tip_id>')
def tips_view(tip_id):
    tip = Tip.query.get_or_404(tip_id)
    user = User.query.get(session['user_id']) if 'user_id' in session else None
    return render_template('tips_view.html', tip=tip, user=user)

@app.route('/tips/<int:tip_id>/edit', methods=['GET', 'POST'])
@login_required
def tips_edit(tip_id):
    tip = Tip.query.get_or_404(tip_id)
    user = User.query.get(session['user_id'])

    if tip.user_id != user.id:
        return redirect(url_for('tips'))

    if request.method == 'POST':
        tip.title = request.form.get('title', tip.title)
        subtitle = request.form.get('subtitle', '')
        tip.content = request.form.get('content', tip.content)
        tags = request.form.get('tags', '')
        category = request.form.get('category')
        if category in ['fashion', 'photography']:
            tip.category = category

        if not tags or not tags.strip():
            return jsonify({'error': 'Tags are required'}), 400
        tip.tags = tags.strip()

        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                if tip.image and not tip.image.startswith('http'):
                    old_path = os.path.join(app.config['POST_UPLOAD_FOLDER'], tip.image)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                image_filename = save_post_picture(file)
                if image_filename:
                    tip.image = image_filename

        try:
            # Try to update subtitle if column exists
            if subtitle:
                try:
                    from sqlalchemy import text
                    db.session.execute(text("UPDATE tip SET subtitle = :subtitle WHERE id = :id"),
                                     {"subtitle": subtitle, "id": tip.id})
                except:
                    pass  # Column might not exist yet

            db.session.commit()
            return jsonify({'success': True, 'message': 'Tip updated!', 'redirect': url_for('tips_view', tip_id=tip.id)}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to update tip'}), 500

    return render_template('tips_edit.html', tip=tip, user=user)

@app.route('/tips/<int:tip_id>/delete', methods=['POST'])
@login_required
def tips_delete(tip_id):
    tip = Tip.query.get_or_404(tip_id)
    if tip.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403

    if tip.image and not tip.image.startswith('http'):
        old_path = os.path.join(app.config['POST_UPLOAD_FOLDER'], tip.image)
        if os.path.exists(old_path):
            os.remove(old_path)

    db.session.delete(tip)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Tip deleted', 'redirect': url_for('tips')}), 200

@app.route('/tips/<int:tip_id>/vote', methods=['POST'])
@login_required
def tip_vote(tip_id):
    tip = Tip.query.get_or_404(tip_id)
    user_id = session['user_id']
    data = request.get_json()
    vote_type = data.get('vote_type')

    if vote_type not in ['like', 'dislike']:
        return jsonify({'error': 'Invalid vote type'}), 400

    # Check if user already voted
    existing_vote = TipVote.query.filter_by(user_id=user_id, tip_id=tip_id).first()

    if existing_vote:
        # If same vote type, remove it (toggle off)
        if existing_vote.vote_type == vote_type:
            db.session.delete(existing_vote)
        else:
            # Change vote type
            existing_vote.vote_type = vote_type
    else:
        # Create new vote
        new_vote = TipVote(user_id=user_id, tip_id=tip_id, vote_type=vote_type)
        db.session.add(new_vote)

    db.session.commit()

    # Get updated counts
    like_count = len([v for v in tip.votes if v.vote_type == 'like'])
    dislike_count = len([v for v in tip.votes if v.vote_type == 'dislike'])

    # Get user's current vote
    user_vote = TipVote.query.filter_by(user_id=user_id, tip_id=tip_id).first()
    user_vote_type = user_vote.vote_type if user_vote else None

    return jsonify({
        'success': True,
        'likes': like_count,
        'dislikes': dislike_count,
        'user_vote': user_vote_type
    }), 200

# ===========================
# ERROR HANDLERS
# ===========================
@app.errorhandler(404)
def not_found(error):
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('404.html', user=user), 404

with app.app_context():
    db.create_all()

    # Add subtitle column to existing tips if it doesn't exist
    try:
        from sqlalchemy import inspect, text
        inspector = inspect(db.engine)
        tip_columns = [col['name'] for col in inspector.get_columns('tip')]

        if 'subtitle' not in tip_columns:
            print("Adding subtitle column to tip table...")
            with db.engine.connect() as conn:
                conn.execute(text('ALTER TABLE tip ADD COLUMN subtitle VARCHAR(500) DEFAULT \'\''))
                conn.commit()
            print("Successfully added subtitle column")

        if 'tags' not in tip_columns:
            print("Adding tags column to tip table...")
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE tip ADD COLUMN tags VARCHAR(500) DEFAULT ''"))
                conn.commit()
            print("Successfully added tags column")

        # Backfill existing tips that have no tags with 'tag'
        with db.engine.connect() as conn:
            conn.execute(text("UPDATE tip SET tags = 'tag' WHERE tags IS NULL OR tags = ''"))
            conn.commit()
        print("Backfilled empty tags with 'tag'")
    except Exception as e:
        print(f"Migration note: {e}")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
