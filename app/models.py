from app import db, bcrypt
import uuid
from sqlalchemy import String

class Role(db.Model):
    id = db.Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))  
    name = db.Column(db.String(50), unique=True, nullable=False)

class Department(db.Model):
    id = db.Column(String, primary_key=True, default=lambda: str(uuid.uuid4())) 
    name = db.Column(db.String(100), unique=True, nullable=False)

class User(db.Model):
    id = db.Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))  
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role_id = db.Column(String, db.ForeignKey('role.id'), nullable=False) 
    department_id = db.Column(String, db.ForeignKey('department.id'), nullable=True)

    role = db.relationship('Role', backref='users')
    department = db.relationship('Department', backref='users')

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Employee(db.Model):
    id = db.Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Float, nullable=False)
    role_id = db.Column(String, db.ForeignKey('role.id'), nullable=False)  
    department_id = db.Column(String, db.ForeignKey('department.id'), nullable=True) 

    role = db.relationship('Role', backref='employees')
    department = db.relationship('Department', backref='employees')

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)