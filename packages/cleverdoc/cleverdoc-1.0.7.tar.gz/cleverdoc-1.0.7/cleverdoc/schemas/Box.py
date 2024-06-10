
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Box_d5c0902eaad9479e9a704c70c883b177.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
