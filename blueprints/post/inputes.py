from flask_wtf import FlaskForm
from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from wtforms import StringField,IntegerField,PasswordField
from wtforms_components import EmailField
from wtforms.validators import DataRequired,Length
from jsonschema import validate
class CreateInput(Inputs):
  json={
      'title':[DataRequired("name field is required")],
      'text':[DataRequired("Email field is required")],
      'image':[DataRequired("An image is required")]
  }

schemaF = {
        "type": "object",
        "properties": {
            "text": {"type": "string"}
        }
    }
class CommentCreate(Inputs):
    json = {
        'text': [DataRequired("Empty!!")],
    }

