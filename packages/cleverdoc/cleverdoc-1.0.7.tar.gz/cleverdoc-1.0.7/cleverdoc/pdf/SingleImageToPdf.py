
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'SingleImageToPdf_cff702a2cb994162a863a15e3eec5f90.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
