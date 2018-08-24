web: gunicorn -w 4 wsgi:app
python: python mig.py db init
python: python mig.py db migrate
python python mig.py db upgrade