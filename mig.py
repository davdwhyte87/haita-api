from extensions import db,migrate
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from app import app
from seeder import Seed
#how to use

migrate.init_app(app,db)
manager=Manager(app)
manager.add_command('db',MigrateCommand)
manager.add_command('hello',Seed())
if __name__=='__main__':
    manager.run()