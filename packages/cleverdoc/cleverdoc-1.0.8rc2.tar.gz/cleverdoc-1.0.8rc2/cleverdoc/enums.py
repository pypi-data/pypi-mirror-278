
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'enums_1b8f7e95ff834aab97838540ba561faa.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
