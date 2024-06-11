
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'StringToKeyValue_4ec6aba4b57e4576b1f1a4b3502f90c2.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
