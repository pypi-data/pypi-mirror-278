
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'LocalPipeline_36127bcaaf3c46898b2d726a737ebff9.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
