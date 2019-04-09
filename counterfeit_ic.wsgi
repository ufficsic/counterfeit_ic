import sys
activate_this = '/home/cic/counterfeit_ic/newenv/bin/activate_this.py'

with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

sys.path.insert(0,"/home/cic/")
from counterfeit_ic import app as application
