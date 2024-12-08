from app import create_app, db
from app.models import Role

def seed_roles():
    roles = ['Admin', 'Manager', 'Employee']
    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            role = Role(name=role_name)
            db.session.add(role)
    db.session.commit()
    print("Roles seeded successfully.")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_roles()