
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'SingleImageToPdf_4387dcdf7fad4959abc5f9373d0d9c92.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
