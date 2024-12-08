from flask import Blueprint, request, jsonify
from app.models import db, Department
from app.utils.decorators import role_required
from uuid import UUID

bp = Blueprint('departments', __name__, url_prefix='/departments')

@bp.route('/', methods=['GET'])
@role_required(['Admin'])
def get_departments():
    departments = Department.query.all()
    return jsonify([{'id': d.id, 'name': d.name} for d in departments]), 200


@bp.route('/create', methods=['POST'])
@role_required(['Admin'])
def create_department():
    data = request.get_json()
    name = data['department_name']
    
    if not name:
        return jsonify({'error': 'Department name is required'}), 400

    if Department.query.filter_by(name=name).first():
        return jsonify({'error': 'Department already exists'}), 400

    department = Department(name=name)
    db.session.add(department)
    db.session.commit()
    return jsonify({'message': 'Department added'}), 201




@bp.route('/<string:department_id>', methods=['PUT'])
@role_required(['Admin'])
def update_department(department_id):
    try:
        department_id = UUID(department_id)
    except ValueError:
        return jsonify({'error': 'Invalid department ID format'}), 400

    data = request.get_json()
    name = data.get('department_name')

    if not name:
        return jsonify({'error': 'Department name is required'}), 400

    department = Department.query.get(department_id)
    if not department:
        return jsonify({'error': 'Department not found'}), 404

    if Department.query.filter(Department.name == name, Department.id != department_id).first():
        return jsonify({'error': 'Another department with this name already exists'}), 400

    department.name = name
    db.session.commit()
    return jsonify({'message': 'Department updated successfully'}), 200



@bp.route('/<string:department_id>', methods=['DELETE'])
@role_required(['Admin'])
def delete_department(department_id):
    try:
        department_uuid = UUID(department_id) 
    except ValueError:
        return jsonify({'error': 'Invalid department ID format'}), 400

    department = Department.query.get(department_uuid)
    if not department:
        return jsonify({'error': 'Department not found'}), 404

    db.session.delete(department)
    db.session.commit()
    return jsonify({'message': 'Department deleted successfully'}), 200