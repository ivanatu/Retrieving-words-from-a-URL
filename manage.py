import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import psycopg2

# from app import app, db
from app import url_app, db

# url_app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(url_app, db)
manager = Manager(url_app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()