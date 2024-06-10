
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'PdfToImage_a3bc948900dd440c8544fa9b819a52e7.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
