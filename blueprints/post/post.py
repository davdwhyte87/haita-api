from flask import Blueprint, request, session, current_app,send_file,send_from_directory
from blueprints.post.inputes import CreateInput,CommentCreate
from login_required import login_required
from blueprints.post.models import Post,Comment,Like
from flask import jsonify
from blueprints.utils import upload_file_encoded
import os
from flask_cors import cross_origin


post=Blueprint('post',__name__,template_folder=None)
ALLOWED_EXTENSIONS=(['png','jpg','jpeg','gif'])


""""
To use the route the ffg fields ae required:
title
text
image
"""
@post.route('/post',methods=('GET','POST'))
@login_required
def create():
    if request.method=="POST":
        uid = request.headers.get('UID')
        inputes=CreateInput(request)
        if inputes.validate():
            post=Post()
            data=request.json
            post.title=data['title']
            post.text=data['text']
            post.user_id=uid
            #upload file
            # fname=upload_file_encoded(data['image'],'post')
            post.image=data['image']
            post.save()
            return jsonify(code=1,message="Successfully created")
        return jsonify(code=0, message="An error occurred", errors=inputes.errors)
    return jsonify(code=0,message="An error occurred")

def allowed_file(filename):
    return'.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@post.route('/posts')
# @login_required
def get_posts():
    from blueprints.model_schema import PostSchema
    posts = Post.query.order_by("id desc").all()
    post_schema = PostSchema(many=True)
    output = post_schema.dump(posts).data
    return jsonify(code=1, data=output)

@post.route('/post/<id>')
def get_post(id):
    from blueprints.model_schema import PostSchema
    post=Post.query.filter_by(id=id).first()
    post_schema=PostSchema()
    output=post_schema.dump(post).data
    return jsonify(code=1,data=output)

@post.route('/hello')
def hello():
    return jsonify({"name":"david","age":43},{"name":"lara","age":23})

@post.route('/post/update/<id>')
@login_required
def update(id):
    from blueprints.model_schema import PostSchema, CommentSchema
    post=Post.query.filter_by(id=id).first()
    post_schema = PostSchema()
    output = post_schema.dump(post).data
    return jsonify(post=output)




@post.route('/image/post/<name>')
def image(name):
    return send_from_directory(current_app.static_folder + "/post", name)


@post.route('/post/<id>/delete',methods=('GET','DELETE'))
@login_required
def delete(id):
    uid = request.headers.get('UID')
    post=Post.query.get(id)
    if uid==post.user_id:
        post.delete()
        return jsonify(code=1)
    else:
        return jsonify(code=0,message="And error occurred, unauthorized action")


#this takes in [ text]
#this function creates a comment for a post
@post.route('/post/<id>/comment',methods=('GET','POST'))
@login_required
def comment(id):
    uid=request.headers.get('UID')
    from blueprints.model_schema import PostSchema, CommentSchema
    if request.method=="POST":
        content = request.json
        inputes = CommentCreate(request)
        if inputes.validate():
            comment=Comment()
            comment.user_id=uid 
            comment.text=content['text']
            comment.post_id=id
            comment.save()
            comment_schema = CommentSchema()
            output = comment_schema.dump(comment).data
            return jsonify(code=1,data=output, message="Comment created successfully")
        else:
            return jsonify(code=0,errors=inputes.errors)

@post.route('/post/<id>/comments')
def all_comment(id):
    from blueprints.model_schema import PostSchema, CommentSchema
    commets= Comment.query.filter_by(post_id=id).order_by("id desc").all()
    comment_schema = CommentSchema(many=True)
    output = comment_schema.dump(commets).data
    return jsonify(code=1,data=output)

@post.route('/post/<id>/like')
@login_required
def like(id):
    uid=request.headers.get('UID')
    print(uid)
    #check if the current user has liked the post
    likex=Like.query.filter_by(post_id=id).filter_by(user_id=uid).first()
    if not likex:
        like=Like()
        like.post_id=id
        like.user_id=uid
        like.save()
        return jsonify(code=1,message="Post Liked")
    else:
       likex.delete() 
       return jsonify(code=0,message="You unliked this post")

@post.route('/my_posts')
# @login_required
def my_posts():
    uid=request.headers.get('UID')
    from blueprints.model_schema import PostSchema
    posts = Post.query.filter_by(user_id=uid)
    post_schema = PostSchema(many=True)
    output = post_schema.dump(posts).data
    return jsonify(code=1, data=output)

@post.route('/find_posts/<id>')
@login_required
def findPosts(id):
    from blueprints.model_schema import PostSchema
    posts = Post.query.filter_by(user_id=id)
    post_schema = PostSchema(many=True)
    output = post_schema.dump(posts).data
    return jsonify(code=1, data=output)
