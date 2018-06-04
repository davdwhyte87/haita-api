
def allowed_file(filename):
    from flask import current_app
    return'.' in filename and filename.rsplit('.',1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def upload_image(image,folder):
    from flask import request,jsonify,current_app
    import os
    if image in request.files:
        file = request.files[image]
        if file.filename == '':
            return jsonify(code=0, message="An image is required")
        if file and allowed_file(file.filename):
            from random import randint
            fname = str(randint(0, 10000093494898585784843989458789488585)) + '.png'
            target = os.path.join(current_app.config['UPLOAD_FOLDER'] + '/'+folder, fname)
            if not os.path.isdir(current_app.config['UPLOAD_FOLDER'] + '/'+folder):
                os.mkdir(current_app.config['UPLOAD_FOLDER'] + "/"+folder)
            file.save(target)
            return fname


def upload_file_encoded(encoded_image,folder):
    from flask import request, jsonify, current_app
    import base64
    import os
    imgData=base64.b64decode(encoded_image)
    from random import randint
    fname = str(randint(0, 10000093494898585784843989458789488585)) + '.png'
    target = os.path.join(current_app.config['UPLOAD_FOLDER'] + '/' + folder, fname)
    if not os.path.isdir(current_app.config['UPLOAD_FOLDER'] + '/' + folder):
        os.mkdir(current_app.config['UPLOAD_FOLDER'] + "/" + folder)
    with open(target, 'wb') as f:
        f.write(imgData)
    f.close()
    return fname

