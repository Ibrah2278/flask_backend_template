from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Mock database - replace with actual database
users_db = {}

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    if data['email'] in users_db:
        return jsonify({'error': 'User already exists'}), 409
    
    users_db[data['email']] = {
        'password': generate_password_hash(data['password'])
    }
    
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    user = users_db.get(data['email'])
    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return jsonify({'message': 'Login successful', 'email': data['email']}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    return jsonify({'message': 'Logout successful'}), 200