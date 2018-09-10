import  os
DEBUG=True
SECRET_KEY="jdksjdksjdksj"
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI="postgresql://postgres:hataguy@localhost:5432/haita"
else:
    SQLALCHEMY_DATABASE_URI = "postgres://clhsswfxcfughm:86a333fc3957d5c234ee6999cf71fd19a3438485a03811d1d474e01f77d78062@ec2-54-235-206-118.compute-1.amazonaws.com:5432/d3j5r4pqh8oah5"

UPLOAD_FOLDER="image"
ALLOWED_EXTENSIONS=(['png','jpg','jpeg','gif'])

ADMIN_NAME="Haita app"
ADMIN_EMAIL="haita@gmail.com"
ADMIN_PASSWORD="quavaleement093"

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS=True
MAIL_USERNAME = 'haitateam100@gmail.com'
MAIL_PASSWORD = "haitaisdope"
