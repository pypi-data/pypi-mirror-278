
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'PdfAssembler_dd97def2f0cb49758d9b9c330dfddd31.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
