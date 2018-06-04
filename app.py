from flask import Flask
from extensions import login_manager
from extensions import db,migrate
from extensions import ma,cors
#blueprints

from blueprints.user import user
from blueprints.post import post

#app setup
app=Flask(__name__,instance_relative_config=True)
app.config.from_object('config.settings')
app.config.from_pyfile('settings.py',silent=True)
#blueprints

app.register_blueprint(user)
app.register_blueprint(post)


#initialize extensions
db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
cors.init_app(app)



#app run
if __name__=='__main__':
    app.run()
