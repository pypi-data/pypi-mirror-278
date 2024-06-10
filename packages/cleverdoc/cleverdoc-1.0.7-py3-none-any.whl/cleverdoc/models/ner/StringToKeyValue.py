
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'StringToKeyValue_939ddf758e8c44f7927019810195f918.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
