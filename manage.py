import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from counterfeit_ic import app
from flask_script import Manager, Server
from application import create_app
from flask_migrate import MigrateCommand

manager = Manager(app)
manager.add_command('db', MigrateCommand)


manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 80)))
)

if __name__ == "__main__":
    manager.run()
