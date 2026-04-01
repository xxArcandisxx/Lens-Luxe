# Lens&Luxe Profile Customization Setup Guide

This guide will walk you through setting up the profile customization system with password management and profile pictures.

## Features Implemented

✅ **User Profile Editing**: Users can customize name, email, phone, interests, and newsletter subscription
✅ **Profile Picture Upload**: Upload and manage profile pictures with preview
✅ **Password Management**: Change password with current password verification
✅ **Password Reset**: Forgot password with email-based reset link (1-hour expiry)
✅ **Security**: Password hashing, token-based reset, form validation

## New Files Created

### Backend
- `app.py` - Updated with new User model fields and routes

### Templates
- `templates/edit_profile.html` - Profile editing page with picture upload
- `templates/change_password.html` - Password change form with strength indicator
- `templates/forgot_password.html` - Request password reset
- `templates/reset_password.html` - Reset password with token validation

### Configuration
- `.env.example` - Email configuration template

### Updated Files
- `requirements.txt` - Added Flask-Mail and python-dotenv
- `templates/dashboard.html` - Added profile picture display and action buttons
- `templates/login.html` - Added "Forgot Password" link

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Email Configuration

**Option A: Using Gmail** (Recommended for testing)

1. Enable 2-Factor Authentication on your Google account
2. Visit https://myaccount.google.com/apppasswords
3. Select "Mail" and your device type
4. Google will generate a 16-character password
5. Create a `.env` file in your project root:

```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
MAIL_DEFAULT_SENDER=noreply@lensandluxe.com
```

**Option B: Using Other Email Services**

Gmail: `smtp.gmail.com`
Outlook: `smtp.office365.com`
Yahoo: `smtp.mail.yahoo.com`
SendGrid: `smtp.sendgrid.net`

### 3. Update app.py

The app automatically loads environment variables from `.env`. Make sure the file is in the root directory.

### 4. Database Migration

Delete the existing `instance/users.db` file or the app will automatically create new columns:

```bash
# First run - Flask will auto-create all columns
python app.py
```

The app will create these new database columns:
- `profile_picture` - Stores filename of uploaded picture
- `reset_token` - For password reset
- `reset_token_expiry` - Token expiry timestamp
- `updated_at` - Tracks last profile update

### 5. File Upload Directory

The app automatically creates the upload directory at: `static/uploads/profiles/`

This folder stores all uploaded profile pictures.

## New Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/profile` | GET | Display profile edit form |
| `/profile` | POST | Save profile changes |
| `/change-password` | GET | Display password change form |
| `/change-password` | POST | Update password |
| `/forgot-password` | GET | Display forgot password form |
| `/forgot-password` | POST | Request password reset email |
| `/reset-password/<token>` | GET | Display reset password form |
| `/reset-password/<token>` | POST | Reset password with token |

## User Flow

### Creating/Editing Profile
1. User clicks "Edit Profile" from dashboard
2. User updates name, email, phone, interests, newsletter preference
3. User optionally uploads a new profile picture
4. User clicks "Save Changes"
5. Profile updates and redirects to dashboard

### Changing Password (Logged In)
1. User clicks "Change Password" from dashboard
2. User enters current password (for verification)
3. User enters new password (min 8 chars, strength indicator shown)
4. User confirms new password
5. Password updates and user is redirected to dashboard

### Password Reset (Forgot Password)
1. User clicks "Forgot Password" on login page
2. User enters their email address
3. System sends reset email with 1-hour token link
4. User clicks link in email
5. User sets new password
6. Password updates and user is redirected to login

## Security Features

✅ **Password Hashing**: Uses werkzeug PBKDF2 hashing
✅ **Reset Tokens**: Unique, urlsafe tokens with 1-hour expiry
✅ **Current Password Verification**: Required for password changes
✅ **File Upload Validation**: 
   - Allowed types: JPG, PNG, GIF
   - Max file size: 5MB
   - Secure filename handling

✅ **CSRF Protection**: Form submissions validated
✅ **Session Management**: Protected routes require login

## Email Testing

For local development, you can configure a test email service:

**Using Mailtrap** (Recommended for testing):
1. Create free account at https://mailtrap.io
2. Get SMTP credentials from their dashboard
3. Update `.env` with Mailtrap credentials

**Using Local SMTP** (No actual email sent):
```python
# In app.py, temporarily add:
app.config['TESTING'] = True
# Emails will be logged to console instead
```

## Troubleshooting

**"SSL: CERTIFICATE_VERIFY_FAILED" error**
- Ensure `MAIL_USE_TLS=True` in `.env`
- For Gmail, make sure you're using an App Password, not your regular password

**"AuthenticationError" from email service**
- Verify credentials in `.env`
- Check if 2FA is enabled (for Gmail)
- Ensure App Password is correct (16 characters)

**Profile pictures not uploading**
- Verify `static/uploads/profiles/` directory exists
- Check file size is under 5MB
- Verify file format is JPG, PNG, or GIF

**Reset emails not being received**
- Check spam folder
- Verify MAIL_USERNAME is correct
- Try sending a test email first

## Optional Enhancements

### Add Email Verification
Send verification email when user changes email address

### Add Profile Picture Gallery
Show user's picture upload history

### Add Password Strength Requirements
Display real-time password strength during change

### Add Rate Limiting
Limit password reset requests to prevent spam

### Add Two-Factor Authentication
Add SMS/TOTP for enhanced security

## Deployment Notes

**Before going to production:**

1. Change `SECRET_KEY` in app.py to a random secure string:
   ```python
   import secrets
   secrets.token_hex(32)
   ```

2. Set `DEBUG=False` in production

3. Use environment variables for all sensitive data:
   - Database URL
   - Mail credentials
   - Secret key

4. Enable HTTPS for profile picture uploads

5. Implement rate limiting on password reset endpoint

6. Add logging for failed login/reset attempts

7. Set up email monitoring/bounce handling

## File Structure

```
Lens&Luxe/
├── app.py (updated)
├── requirements.txt (updated)
├── .env (create from .env.example)
├── static/
│   ├── uploads/
│   │   └── profiles/ (auto-created)
│   ├── styles.css
│   └── script.js
├── templates/
│   ├── dashboard.html (updated)
│   ├── edit_profile.html (new)
│   ├── change_password.html (new)
│   ├── forgot_password.html (new)
│   ├── reset_password.html (new)
│   ├── login.html (updated)
│   └── ... other templates
├── instance/
│   └── users.db (will have new columns)
└── .env.example (new)
```

## Testing Checklist

- [ ] User can edit profile name, email, phone
- [ ] User can change interests/newsletter preference
- [ ] User can upload profile picture
- [ ] Uploaded picture displays on dashboard
- [ ] User can change password (with current password required)
- [ ] Password strength indicator works
- [ ] User can request password reset
- [ ] Reset email is received
- [ ] Reset link is valid for 1 hour
- [ ] Reset link is invalid after 1 hour
- [ ] User can reset password with link
- [ ] File upload validation works (wrong file types rejected)
- [ ] File size limit works (>5MB rejected)
- [ ] Profile picture is displayed as circular thumbnail
- [ ] Old profile picture is deleted on upload
- [ ] Navigation shows "Edit Profile" and "Change Password" links
- [ ] All forms have proper error handling

## Support & Questions

For issues or questions, refer to:
- Flask-Mail documentation: https://flask-mail.readthedocs.io/
- Werkzeug security: https://werkzeug.palletsprojects.com/security/
- SQLAlchemy docs: https://docs.sqlalchemy.org/
