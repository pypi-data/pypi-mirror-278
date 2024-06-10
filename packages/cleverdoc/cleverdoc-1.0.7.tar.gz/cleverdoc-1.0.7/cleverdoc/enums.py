
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'enums_0b6aa3f75fcc42429e11c10441deb6e3.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
