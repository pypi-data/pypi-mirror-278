
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'ImageDrawBoxes_7409fce39dac4d7ea6ffb36a116d9ce9.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
