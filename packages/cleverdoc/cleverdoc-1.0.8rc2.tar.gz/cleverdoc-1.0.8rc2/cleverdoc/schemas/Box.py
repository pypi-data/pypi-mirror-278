
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Box_d7ec18fc433b401ba3e0caffe168825e.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
