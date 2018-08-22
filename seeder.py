from blueprints.admin.models import Admin
from flask import current_app
from flask_script import Command


class Seed(Command):
    def run(self):
        print("hello babe")
        admin = Admin.query.all()
        if len(admin) > 0:
            print("admin exists")
            return
        else:
            name = current_app.config['ADMIN_NAME']
            email = current_app.config['ADMIN_EMAIL']
            password = current_app.config['ADMIN_PASSWORD']
            admin=Admin()
            admin.name = name
            admin.email = email
            admin.encrypt_password(password)
            admin.save()
            return



