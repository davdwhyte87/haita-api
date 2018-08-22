from flask_wtf import FlaskForm
from flask_inputs import Inputs
from blueprints.admin.models import Admin
from wtforms import StringField,IntegerField,PasswordField
from wtforms_components import EmailField
from wtforms.validators import DataRequired,Length,ValidationError

def email_exists(form,field):
    print("quiccy")
    print(type(field))
    admin=Admin.query.filter_by(email=field.data).first()
    if admin:
        raise ValidationError("Email already exists")

class LoginInput(Inputs):
   json={
       'email': [DataRequired("Email field is required")],
       'password': [DataRequired("Password is required")]
   }

class CreateInput(Inputs):
    json={
        'email':[DataRequired("Email is required"),email_exists],
        'name':[DataRequired("Name is required")],
        'password':[DataRequired("A Passsowrd is required"),Length(min=5,max=100)]
    }