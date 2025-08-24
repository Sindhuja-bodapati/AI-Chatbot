import os
import secrets
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask Secret Key (used for session encryption)
SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)

# Google Gemini API Key (from .env or system env)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Database configuration (adjust values as per your setup)
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'your_username'),
    'password': os.getenv('DB_PASSWORD', 'your_password'),
    'database': os.getenv('DB_NAME', 'chatbot_db')
}

# Application settings
APP_SETTINGS = {
    'debug': os.getenv('FLASK_DEBUG', 'True') == 'True',
    'host': os.getenv('FLASK_RUN_HOST', '0.0.0.0'),
    'port': int(os.getenv('FLASK_RUN_PORT', 5000))
}

# JWT Configuration
JWT_CONFIG = {
    'token_expiration_hours': int(os.getenv('JWT_EXP_HOURS', 24))
}

# Rate limiting settings
RATE_LIMIT = os.getenv('RATE_LIMIT', "200 per day, 50 per hour")

# CORS settings
CORS_CONFIG = {
    'resources': {
        r"/api/*": {
            "origins": ["http://localhost:*", "http://127.0.0.1:*"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    }
}
