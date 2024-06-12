
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'OcrOutput_c0c58cdcb9494bf095ea781ae8b5c1c3.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
