from flask import Blueprint, request, make_response,current_app,send_file,session
from login_required import login_required
from blueprints.user.inputes import RegisterInput,LoginInput,UpdateForm
from blueprints.user.models import User,Token
from blueprints.model_schema import UserSchema
from flask import jsonify
from blueprints.utils import upload_file_encoded
import os
from random import randint

user=Blueprint('user',__name__,template_folder='templates')


def allowed_file(filename):
    return'.' in filename and filename.rsplit('.',1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


""""
In to use the register route, you need:
name
email
phone
password
"""
@user.route('/register',methods=('GET','POST'))
def register():
    if request.method=="POST":
        inputs = RegisterInput(request)
        if  inputs.validate():
            data=request.json
            user = User()
            user.encrypt_password(data['password'])
            user.name =  data['name']
            user.email = data['email']
            user.phone = data['phone']
            user.code = randint(0, 90000)
            user.save()
            return jsonify(code=1,message="User created Successfully")
        else:
            return jsonify(code=0, errors=inputs.errors,message="An error occured")
    return "done"

@user.route('/confirm/<code>')
def confirm(code):
    user = User.query.filter_by(code=code).first()
    if user:
        user.confirmed=1
        user.save()
        return jsonify(code=1,message="Confirmed")
    else:
        return jsonify(code=0,message="An error occurred")

@user.route('/forgotpass',methods=('GET','POST'))
def forgotpass():
    data=request.json
    email=data['email']
    code=randint(0,90000)
    user = User.query.filter_by(email=email).first()
    if user:
        user.code=code
        user.save()
        #send code to mail
        return jsonify(code=1,message="Code sent to mail")
    else:
        return jsonify(code=0,message="An error occurred. email does not belong to a user")


@user.route('/forgotpass/changepass',methods=('GET','POST'))
def forgotpass_changepass():
    data=request.json
    password=data['password']
    code=data['code']
    user = User.query.filter_by(code=code).first()

    if user:
        user.encrypt_password(data['password'])
        user.save()
        api_token = Token.query.filter_by(user_id=user.id).first()
        if api_token:
            api_token.delete()
        session['user_id']=""
        return jsonify(code=1,message="password changed successfully")
    else:
        return jsonify(code=0,message="An error occurred")

# takes in name,phone,bio, maybe an encoded image
@user.route('/user/<id>/update',methods=('GET','POST'))
@login_required
def update(id):
    if request.method=="POST":
        user = User.query.filter_by(id=id).first()
        inputes=UpdateForm(request)
        if not user:
            return jsonify(code=0,message="User not fount")
        if inputes.validate():
            data=request.json
            user.name = data['name']
            user.phone = data['phone']
            user.bio=data['bio']
            if data['image']:
                fname=upload_file_encoded(data['image'],'user')
                user.image=fname
            user.save()
            return jsonify(code=1,message="Updated successfully")
        else:
            return jsonify(code=0, message="An error occured", errors=inputes.errors )
    return jsonify(code=0, message="An error occurred" )

""""
In to use the register route, you need:
email
password
"""
@user.route('/login',methods=('GET','POST'))
def login():
    print(request.cookies.get('user',0))
    if request.method=="POST" :
        form = LoginInput(request)
        if form.validate():
            data=request.json
            email = data['email']
            user=User.query.filter_by(email=email).first()
            if user:
                if user.authenticate(user.password, data['password']):
                    import os
                    tk = Token()
                    tk.api_token = os.urandom(100)
                    tk.set_dates()
                    tk.user_id = user.id
                    tk.save()
                    return jsonify(code=1,token=tk.api_token)
                else:
                    return jsonify(code=0,message="Password or email is wrong")
            else:
                return jsonify(code=0,message="This user does not exist")
        else:
            return jsonify(code=0,success=False, errors=form.errors)

@user.route('/image/user/<name>')
def image(name):
    return send_file('image\\user\\'+name)


@user.route('/user/all')
@login_required
def all():
    users = User.query.all()
    post_schema = UserSchema(many=True)
    output = post_schema.dump(users).data
    return jsonify(users=output)


@user.route('/user')
@login_required
def getUser():
    id=session['user_id']
    user=User.query.filter_by(id=id).first()
    if user:
        user_schema=UserSchema()
        output=user_schema.dump(user).data
        return jsonify(code=1,user=output)
    return jsonify(code=0,message="This user does not exist")

@user.route('/')
def hello():
    return "hello this is the user module"