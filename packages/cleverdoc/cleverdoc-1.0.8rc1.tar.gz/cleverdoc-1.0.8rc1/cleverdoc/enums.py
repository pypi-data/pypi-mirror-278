
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'enums_72a4e3593a6049849d77779a2084f1df.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
