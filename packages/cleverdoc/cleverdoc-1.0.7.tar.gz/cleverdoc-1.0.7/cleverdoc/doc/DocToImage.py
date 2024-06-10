
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'DocToImage_76d63861263d480c9e12bb5376a6ce30.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
