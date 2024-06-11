
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'ImageDrawBoxes_f3997be24b394399885eae69f6bc98bb.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
