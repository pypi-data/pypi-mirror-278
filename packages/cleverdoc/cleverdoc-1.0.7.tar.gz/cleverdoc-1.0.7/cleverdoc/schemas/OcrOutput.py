
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'OcrOutput_d1949d92d4a14344b9735954cfbfc5f7.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
