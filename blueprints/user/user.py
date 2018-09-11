from flask import Blueprint, request, make_response,current_app,send_file,session,render_template,send_from_directory
from login_required import login_required
from blueprints.user.inputes import RegisterInput,LoginInput,UpdateForm,ChangePass
from blueprints.user.models import User,Token
from blueprints.model_schema import UserSchema
from flask import jsonify
from blueprints.utils import upload_file_encoded
import os
from random import randint
from flask_cors import cross_origin
from flask_mail import Message
from extensions import mail

user=Blueprint('user',__name__,template_folder='templates')


def allowed_file(filename):
    return'.' in filename and filename.rsplit('.',1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


""""
In to use the register route, you need:
name
email
phone
password
username
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
            user.uname=data['uname']
            user.code = randint(0, 90000)
            msg = Message("Hello",
                          sender=("Haita", "haitateam100@gmail.com"),recipients=[user.email])
            msg.html = render_template("mail.html",code=user.code)
            try:
                mail.send(msg)
            except:
                return jsonify(code=0, errors=inputs.errors, message="An error occured")
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
        return jsonify(code=0,message="An error occurred, This code doesn't belong to any user")

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
        msg = Message("Hello",
                      sender=("Haita", "haitateam100@gmail.com"), recipients=[email])
        msg.html = render_template("mail.html", code=user.code)
        mail.send(msg)
        return jsonify(code=1,message="Code sent to mail")
    else:
        return jsonify(code=0,message="An error occurred. email does not belong to a user")


@user.route('/forgotpass/changepass',methods=('GET','POST'))
def forgotpass_changepass():
    if request.method=="POST":
        changepassInputes=ChangePass(request)
        if changepassInputes.validate():
            data=request.json
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
                return jsonify(code=0,message="An error occurred, this code does not belong to a user")
        else:
           return jsonify(code=0,errors=changepassInputes.errors ,message="An error occured")

# takes in name,phone,bio, maybe an encoded image
@user.route('/user/<id>/update',methods=('GET','PUT'))
@login_required
def update(id):
    if request.method=="PUT":
        print(request.json)
        user = User.query.filter_by(id=id).first()
        inputes=UpdateForm(request)
        if not user:
            return jsonify(code=0,message="User not fount")
        if inputes.validate():
            data=request.json
            user.name = data['name']
            if "phone" in data:
                user.phone = data['phone']
            if "bio" in data:
                user.bio=data['bio']
            if "uname" in data:
                user.uname=data['uname']
            if "image" in data:
                fname=upload_file_encoded(data['image'],'user')
                user.image=fname
            user.save()
            return jsonify(code=1,message="Updated successfully")
        else:
            return jsonify(code=0, message="An error occured", errors=inputes.errors )
    return jsonify(code=0, message="An error occurred")

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
                if user.confirmed == 0:
                    return jsonify(code=0, message="You need to confirm your account. Please check your mail")
                if user.authenticate(user.password, data['password']):
                    import os
                    tk = Token()
                    tk.api_token = os.urandom(100)
                    tk.set_dates()
                    tk.user_id = user.id
                    tk.save()
                    return jsonify(code=1,token=tk.api_token,message="You are now logged in",user_id=user.id)
                else:
                    return jsonify(code=0,message="Password or email is wrong")
            else:
                return jsonify(code=0,message="This user does not exist")
        else:
            return jsonify(code=0,message="An error occurred", errors=form.errors)

@user.route('/image/user/<name>')
def image(name):
    print(current_app.static_folder)
    return send_from_directory(current_app.static_folder+"/user",name)


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
    uid = request.headers.get('UID')
    id=uid
    user=User.query.filter_by(id=id).first()
    if user:
        user_schema=UserSchema()
        output=user_schema.dump(user).data
        return jsonify(code=1,data=output)
    return jsonify(code=0,message="This user does not exist")

@user.route('/')
def hello():
    return "hello this is the user module"

@user.route('/checksignin')
@login_required
def checksignin():
    return jsonify(code=1)
