web: gunicorn -w 4 wsgi:app
init: python mig.py db init
migrate: python mig.py db migrate
upgrade: python mig.py db upgrade