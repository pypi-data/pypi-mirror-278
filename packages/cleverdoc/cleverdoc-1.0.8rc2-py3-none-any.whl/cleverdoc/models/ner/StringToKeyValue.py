
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'StringToKeyValue_bdc9d5e49cf34d4c861d404747ec3c95.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
