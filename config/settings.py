import  os
from dotenv import load_dotenv
load_dotenv()

DEBUG= os.getenv('DEBUG')
SECRET_KEY= os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI= os.getenv('SQLALCHEMY_DATABASE_URI')

UPLOAD_FOLDER= os.getenv('UPLOAD_FOLDER')
ALLOWED_EXTENSIONS= os.getenv('ALLOWED_EXTENSIONS')

ADMIN_NAME= os.getenv('ADMIN_NAME')
ADMIN_EMAIL= os.getenv('ADMIN_EMAIL')
ADMIN_PASSWORD= os.getenv('ADMIN_PASSWORD')

# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 587
# MAIL_USE_SSL = False
# MAIL_USE_TLS=True
# MAIL_USERNAME = 'haitateam100@gmail.com'
# MAIL_PASSWORD = "haitaisdope"

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDGRID_DEFAULT_FROM = os.getenv('SENDGRID_DEFAULT_FROM')
DB_URL = os.getenv('DB_URL')
