
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'PdfDocument_38165005ddbd4471b194dda906d9175c.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
