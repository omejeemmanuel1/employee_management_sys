# Employee Management System

This is a Python Flask-based RESTful API for managing employees, roles, and departments, featuring Role-Based Access Control (RBAC). It supports user authentication, CRUD operations, and role management.

Setup Instructions

1. Clone the Repository:

git clone [https://github.com/omejeemmanuel1/employee_management_sys.git]
cd employee_management_task

2. Set Up Virtual Environment:

python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install Dependencies:

pip install Flask Flask-JWT-Extended Flask-Bcrypt Flask-SQLAlchemy Flask-Migrate

4. Database Setup:
 • Update config.py with your database connection details (SQLite is used by default).
 • Run the migrations:

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

5. Seed Roles:

Run the following script to add default roles:

python seed_roles.py

Endpoints

Authentication

Signup
 • POST /auth/signup
 • Description: Register a new user.
 • Payload:

{
    "username": "john_doe",
    "email": "<john.doe@example.com>",
    "password": "12345",
    "role": "Admin"
}

 • Response:

{
    "message": "User created successfully"
}

Login
 • POST /auth/login
 • Description: Login and retrieve a JWT token.
 • Payload:

{
    "email": "<john.doe@example.com>",
    "password": "12345"
}

 • Response:

{
    "access_token": "<jwt_token>"
}

Get User Details
 • GET /auth/user
 • Description: Fetch the details of the currently logged-in user.
 • Headers:
 • Authorization: Bearer <access_token>
 • Response:

{
    "id": 1,
    "username": "john_doe",
    "email": "<john.doe@example.com>",
    "role": "Admin",
    "department": "Engineering"
}

Department Management

Get Departments
 • GET /departments/
 • Description: Retrieve a list of all departments.
 • Headers:
 • Authorization: Bearer <access_token>
 • Response:

[
    {
        "id": 1,
        "name": "Engineering"
    },
    {
        "id": 2,
        "name": "HR"
    }
]

Create Department
 • POST /departments/create
 • Description: Add a new department.
 • Headers:
 • Authorization: Bearer <access_token>
 • Payload:

{
    "name": "Finance"
}

 • Response:

{
    "message": "Department added"
}

Update Department
 • PUT /departments/<department_id>
 • Description: Update an existing department’s name.
 • Headers:
 • Authorization: Bearer <access_token>
 • Payload:

{
    "name": "Updated Department Name"
}

 • Response:

{
    "message": "Department updated successfully"
}

Delete Department
 • DELETE /departments/<department_id>
 • Description: Delete a department.
 • Headers:
 • Authorization: Bearer <access_token>
 • Response:

{
    "message": "Department deleted successfully"
}

Roles Management

Get Roles
 • GET /roles/
 • Description: Retrieve a list of all roles.
 • Headers:
 • Authorization: Bearer <access_token>
 • Response:

[
    {
        "id": "uuid",
        "name": "Admin"
    },
    {
        "id": "uuid",
        "name": "Manager"
    },
    {
        "id": "uuid",
        "name": "Employee"
    }
]

Create Role
 • POST /roles/create
 • Description: Create a new role.
 • Headers:
 • Authorization: Bearer <access_token>
 • Payload:

{
    "name": "Manager"
}

 • Response:

{
    "message": "Role created successfully"
}

Update Role
 • PUT /roles/<role_id>
 • Description: Update an existing role’s name.
 • Headers:
 • Authorization: Bearer <access_token>
 • Payload:

{
    "name": "Super Admin"
}

 • Response:

{
    "message": "Role updated successfully"
}

Delete Role
 • DELETE /roles/<role_id>
 • Description: Delete a role.
 • Headers:
 • Authorization: Bearer <access_token>
 • Response:

{
    "message": "Role deleted successfully"
}

Employee Management

Get All Employees
 • GET /employees/
 • Description: Retrieve a list of all employees.
 • Headers:
 • Authorization: Bearer <access_token>
 • Response:

[
    {
        "id": "uuid",
        "username": "john_doe",
        "email": "john.doe@example.com",
        "role": "Admin",
        "department": "Engineering"
    }
]

Create Employee
 • POST /employees/create
 • Description: Add a new employee.
 • Headers:
 • Authorization: Bearer <access_token>
 • Payload:

{
    "username": "jane_doe",
    "email": "<jane.doe@example.com>",
    "password": "12345",
    "hire_date": "2024-01-01",
    "salary": 50000,
    "role_id": "uuid",
    "department_id": "uuid"
}

 • Response:

{
    "message": "Employee added successfully"
}

Update Employee
 • PUT /employees/<employee_id>
 • Description: Update an existing employee’s details.
 • Headers:
 • Authorization: Bearer <access_token>
 • Payload:

{
    "username": "jane_updated",
    "email": "<jane.updated@example.com>",
    "password": "newpassword123",
    "hire_date": "2024-02-01",
    "salary": 60000,
    "role_id": "uuid",
    "department_id": "uuid"
}

 • Response:

{
    "message": "Employee updated successfully"
}

Delete Employee
 • DELETE /employees/<employee_id>
 • Description: Delete an employee.
 • Headers:
 • Authorization: Bearer <access_token>
 • Response:

{
    "message": "Employee deleted successfully"
}

Technologies Used
 • Flask: Python web framework.
 • Flask-JWT-Extended: For authentication and authorization.
 • Flask-SQLAlchemy: ORM for database management.
 • Flask-Migrate: For database migrations.
 • SQLite: Default database for development.
