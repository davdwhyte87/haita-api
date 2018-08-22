from flask import Blueprint,request,jsonify
from admin_login_required import admin_login_required
from blueprints.admin.models import Admin,AdminToken
from blueprints.admin.inputes import LoginInput,CreateInput
from blueprints.post.models import Post
from blueprints.model_schema import PostSchema
from blueprints.user.models import User
admin=Blueprint('admin',__name__,template_folder=None)

#automatically create an admin if there is no admin


#login admins. takes in email,password
@admin.route('/admin/login',methods=('GET','POST'))
def login():
    if request.method=="POST" :
        form = LoginInput(request)
        if form.validate():
            data=request.json
            email = data['email']
            admin=Admin.query.filter_by(email=email).first()
            if admin:
                if admin.authenticate(admin.password, data['password']):
                    import os
                    atk = AdminToken()
                    atk.api_token = os.urandom(100)
                    atk.set_dates()
                    atk.admin_id= admin.id
                    atk.save()
                    return jsonify(code=1,token=atk.api_token)
                else:
                    return jsonify(code=0,message="Password or email is wrong")
            else:
                return jsonify(code=0,message="This Admin does not exist")
        else:
            return jsonify(code=0,success=False, errors=form.errors)


@admin.route('/admin/create',methods=('GET','POST'))
@admin_login_required
def create():
    if request.method == "POST":
        form=CreateInput(request)
        if form.validate():
            data=request.json
            admin = Admin()
            admin.name = data['name']
            admin.email = data['email']
            admin.encrypt_password(data['password'])
            admin.save()
            return jsonify(code=1,message="Admin created successfully")
        else:
            return jsonify(code=0,message="An error occured",errors=form.errors)

@admin.route('/admin/posts')
def all_posts():
    posts=Post.query.all()
    post_schema=PostSchema(many=True)
    output=post_schema.dump(posts).data
    return jsonify(code=1,data=output)

@admin.route('/admin/posts/user/<id>')
def user_posts(id):
    posts=Post.query.filter_by(user_id=id).all()
    post_schema = PostSchema(many=True)
    output = post_schema.dump(posts).data
    return jsonify(code=1, data=output)

#deletes a post with $id
@admin.route('/admin/post/<id>/delete')
def delete_post(id):
    post=Post.query.filter_by(id=id).first()
    post.delete()
    return jsonify(code=1,message="Post deleted")

#disables a user with $id
@admin.route('/admin/user/<id>/disable')
def disable_user(id):
    user=User.query.filter_by(id=id).first()
    user.confirmed=0
    user.save()
    return jsonify(code=1,message="The user has been disabled")

#delete a user from platform
@admin.route('/admin/user/<id>/delete')
def delete_user(id):
    return jsonify(code=1,message="The user has been deleted")
