
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'ImageDrawBoxes_f9ad6f9ebc174cf7ad4a11cd3cb7ae1a.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
