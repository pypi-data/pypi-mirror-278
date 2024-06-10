
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'ImageToString_f13f006875b545f9999e0ca89aa81ce0.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
