from flask import Flask
import seeder
from extensions import login_manager
from extensions import db,migrate
from extensions import ma,cors,mail
from extensions import send_grid
#blueprints

from blueprints.user import user
from blueprints.post import post
from blueprints.admin import admin

#app_ setup
app=Flask(__name__,instance_relative_config=True,static_folder="image")
app.config.from_object('config.settings')
app.config.from_pyfile('settings.py',silent=True)
#blueprints

app.register_blueprint(user)
app.register_blueprint(post)
app.register_blueprint(admin)


#initialize extensions
db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
cors.init_app(app)
send_grid.init_app(app)
#initial app_ function checks

def creat_app(conf):
    return app.run(conf)

print(app.config['DB_URL'])
#app_ run
if __name__=='__main__':
    app.run()
