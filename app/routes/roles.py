from flask import Blueprint, request, jsonify
from app.models import db, Role
from app.utils.decorators import role_required
from uuid import UUID

bp = Blueprint('roles', __name__, url_prefix='/roles')

@bp.route('/', methods=['GET'])
@role_required(['Admin'])
def get_roles():
    roles = Role.query.all()
    return jsonify([{'id': str(r.id), 'name': r.name} for r in roles]), 200


@bp.route('/create', methods=['POST'])
@role_required(['Admin'])
def create_role():
    data = request.get_json()
    name = data.get('role_name')
    if not name:
        return jsonify({'error': 'Role name is required'}), 400

    if Role.query.filter_by(name=name).first():
        return jsonify({'error': 'Role already exists'}), 400

    new_role = Role(name=name)
    db.session.add(new_role)
    db.session.commit()
    return jsonify({'message': f'Role "{name}" created successfully'}), 201


@bp.route('/<string:role_id>', methods=['PUT'])
@role_required(['Admin'])
def update_role(role_id):
    try:
        role_uuid = UUID(role_id)  
    except ValueError:
        return jsonify({'error': 'Invalid role ID format'}), 400

    data = request.get_json()
    name = data.get('role_name')
    if not name:
        return jsonify({'error': 'New role name is required'}), 400

    role = Role.query.get(role_uuid)  
    if not role:
        return jsonify({'error': 'Role not found'}), 404

    role.name = name
    db.session.commit()
    return jsonify({'message': f'Role updated to "{name}" successfully'}), 200


@bp.route('/<string:role_id>', methods=['DELETE'])
@role_required(['Admin'])
def delete_role(role_id):
    try:
        role_uuid = UUID(role_id) 
    except ValueError:
        return jsonify({'error': 'Invalid role ID format'}), 400

    role = Role.query.get(role_uuid) 
    if not role:
        return jsonify({'error': 'Role not found'}), 404

    db.session.delete(role)
    db.session.commit()
    return jsonify({'message': 'Role deleted successfully'}), 200