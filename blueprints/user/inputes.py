from flask_wtf import FlaskForm
from flask_inputs import Inputs
from wtforms import StringField,IntegerField,PasswordField
from wtforms_components import EmailField
from wtforms.validators import DataRequired,Length,ValidationError


def email_exists(form,field):
    from blueprints.user.user import User
    print(type(field))
    admin=User.query.filter_by(email=field.data).first()
    if admin:
        raise ValidationError("Email already exists")

def uname_exists(form,field):
    from blueprints.user.user import User
    print(type(field))
    admin=User.query.filter_by(uname=field.data).first()
    if admin:
        raise ValidationError("The username has been taken")

class RegisterInput(Inputs):
  json={
      'name':[DataRequired("name field is required")],
      'email':[DataRequired("Email field is required"),email_exists],
      'phone':[DataRequired("phone field is required")],
      'password':[DataRequired("Password is required")],
      'uname':[DataRequired("A username is required")]
  }

class LoginInput(Inputs):
   json={
       'email': [DataRequired("Email field is required")],
       'password': [DataRequired("Password is required")]
   }

class UpdateForm(Inputs):
    json = {
        'name': [DataRequired("name field is required")],
    }

class ChangePass(Inputs):
     json={
       'password': [DataRequired("Password field is required")],
       'code': [DataRequired("The code is required")]
   }