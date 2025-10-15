import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
    
    # Google Drive API
    GOOGLE_DRIVE_CREDENTIALS_FILE = os.environ.get('GOOGLE_DRIVE_CREDENTIALS_FILE')
    GOOGLE_DRIVE_TOKEN_FILE = os.environ.get('GOOGLE_DRIVE_TOKEN_FILE')
    
    # Email configuration
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    FROM_EMAIL = os.environ.get('FROM_EMAIL', 'noreply@studentfiles.com')
    
    # Database
    USERS_FILE = 'users_data.json'
