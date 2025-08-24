from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import jwt
import datetime
from functools import wraps
import google.generativeai as genai
from werkzeug.security import generate_password_hash, check_password_hash
import config
import secrets
import os 
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key="AIzaSyBwkyGZwX_rTH7AxX1oImRmh1Xar0wu5wk")



genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Flask
app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {"origins": ["http://localhost:5000"]},
    r"/": {"origins": "*"}
})

# Configuration
app.config['SECRET_KEY'] = secrets.token_hex(32)  or 'dev-fallback-key'

# Gemini AI Setup
try:
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"⚠️ Gemini initialization failed: {str(e)}")
    model = None

# In-memory Database (Replace with real DB in production)
users_db = {}

# Helper Functions
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token required!'}), 401
            
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = users_db.get(data['email'])
            if not current_user:
                raise ValueError("User not found")
        except Exception as e:
            print(f"🔴 Token verification failed: {str(e)}")
            return jsonify({'message': 'Invalid token'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

# Routes
@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

@app.route('/debug/users')
def debug_users():
    """Development-only endpoint"""
    return jsonify({
        'users': {email: {**user, 'password': '[HASHED]'} 
                 for email, user in users_db.items()},
        'count': len(users_db)
    })

@app.route('/api/signup', methods=['POST'])
def signup():
    required_fields = ['name', 'email', 'password']
    data = request.get_json()
    
    if not all(field in data for field in required_fields):
        return jsonify({'message': f'Missing: {required_fields}'}), 400
        
    if data['email'] in users_db:
        return jsonify({'message': 'Email already registered'}), 409  # 409 Conflict
        
    users_db[data['email']] = {
        'name': data['name'],
        'email': data['email'],
        'password': generate_password_hash(data['password'])
    }
    
    print(f"🟢 New user: {data['email']}")
    return jsonify({'message': 'Registration successful'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email and password required'}), 400
        
    user = users_db.get(data['email'])
    
    if not user or not check_password_hash(user['password'], data['password']):
        print(f"🔴 Failed login for: {data['email']}")
        return jsonify({'message': 'Invalid credentials'}), 401
        
    token = jwt.encode({
        'email': user['email'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'])
    
    return jsonify({
        'token': token,
        'user': {'name': user['name'], 'email': user['email']}
    })

@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message.strip():
            return jsonify({"error": "Message is required"}), 400

        # define model FIRST
        model = genai.GenerativeModel("gemini-1.5-flash")

        # now generate response
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})

    except Exception as e:
        print("Error in /api/chat:", str(e))
        return jsonify({"error": "Failed to generate response"}), 500

if __name__ == "__main__":
    app.run(
        debug=config.APP_SETTINGS.get('debug', True),
        host=config.APP_SETTINGS.get('host', '0.0.0.0'),
        port=config.APP_SETTINGS.get('port', 5000)
    )