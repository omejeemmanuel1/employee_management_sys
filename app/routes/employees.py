from flask import Blueprint, request, jsonify
from app.models import db, Employee, Role
from app.utils.decorators import role_required
from datetime import datetime
from uuid import UUID  

bp = Blueprint('employees', __name__, url_prefix='/employees')

@bp.route('/', methods=['GET'])
@role_required(['Admin', 'Manager'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([{'id': str(e.id), 'username': e.username, 'email': e.email} for e in employees]), 200


@bp.route('/create', methods=['POST'])
@role_required(['Admin'])
def create_employee():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d')  
    salary = data['salary']
    role_name = data.get('role', 'Employee') 

    if Employee.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    if Employee.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return jsonify({'message': 'Role not found'}), 400

    employee = Employee(
        username=username,
        email=email,
        password=password,
        hire_date=hire_date,
        salary=salary,
        role_id=role.id
    )
    employee.set_password(password) 

    db.session.add(employee)
    db.session.commit()

    return jsonify({'message': 'Employee added'}), 201

@bp.route('/<string:employee_id>', methods=['PUT'])
@role_required(['Admin'])
def update_employee(employee_id):
    try:
        employee_uuid = UUID(employee_id)  
    except ValueError:
        return jsonify({'error': 'Invalid employee ID format'}), 400

    data = request.get_json()
    employee = Employee.query.get_or_404(employee_uuid)
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    hire_date = data.get('hire_date')
    salary = data.get('salary')
    role_name = data.get('role')

    if username:
        employee.username = username
    if email:
        employee.email = email
    if password:
        employee.set_password(password)
    if hire_date:
        employee.hire_date = datetime.strptime(hire_date, '%Y-%m-%d')
    if salary:
        employee.salary = salary
    if role_name:
        role = Role.query.filter_by(name=role_name).first()
        if role:
            employee.role_id = role.id

    db.session.commit()
    return jsonify({'message': 'Employee updated'}), 200

@bp.route('/<string:employee_id>', methods=['DELETE'])
@role_required(['Admin'])
def delete_employee(employee_id):
    try:
        employee_uuid = UUID(employee_id) 
    except ValueError:
        return jsonify({'error': 'Invalid employee ID format'}), 400

    employee = Employee.query.get_or_404(employee_uuid)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted'}), 200