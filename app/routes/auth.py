import uuid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.models import db, User, Role
from uuid import UUID

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    role_name = data['role']

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return jsonify({'error': 'Invalid role'}), 400

    role_id = uuid.UUID(str(role.id))  

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    user = User(username=username, email=email, role_id=role_id)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201



@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    role_name = user.role.name if user.role else None 

    identity = f"{user.id}_{role_name}"

    access_token = create_access_token(identity=identity)
    return jsonify({'access_token': access_token}), 200


@bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    current_user = get_jwt_identity()

    try:
        user_id_str, role_name = current_user.split('_', 1)
    except ValueError:
        return jsonify({'error': 'Invalid identity format'}), 400

    try:
        user_id = UUID(user_id_str)
    except ValueError:
        return jsonify({'error': 'Invalid user ID format'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_data = {
        'id': str(user.id), 
        'username': user.username,
        'email': user.email,
        'role': role_name,
    }
    return jsonify(user_data), 200