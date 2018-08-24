web: gunicorn -w 4 wsgi:app
web: python mig.py db init
web: python mig.py db migrate
web: python mig.py db upgrade