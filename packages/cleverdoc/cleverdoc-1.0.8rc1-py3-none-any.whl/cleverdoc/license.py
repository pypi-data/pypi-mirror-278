
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'license_6e34bb9c29ad493c9a85f61c6316ac97.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
