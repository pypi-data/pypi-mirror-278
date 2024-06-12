
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'BinaryToImage_0c109627955d4d82889af2b7422075dc.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
