
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'NerMerger_d8d20a076986403c8278bf403ae20aa1.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
