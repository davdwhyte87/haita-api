from blueprints.post.models import Post,Comment
from blueprints.user.models import User
from extensions import ma,db
from marshmallow import fields

class UserSchema(ma.ModelSchema):
    class Meta:
        model=User
        fields=('id','name','email','image')
        sqla_session = db.session
class CommentSchema(ma.ModelSchema):
    class Meta:
        model=Comment
        sqla_session=db.session
    user=ma.Nested(UserSchema)

class PostSchema(ma.ModelSchema):
    class Meta:
        model=Post
        sqla_session=db.session
    user=ma.Nested(UserSchema)
    comment=ma.Nested(CommentSchema,many=True)
    





