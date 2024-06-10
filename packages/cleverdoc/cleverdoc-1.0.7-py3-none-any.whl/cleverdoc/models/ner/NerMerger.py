
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'NerMerger_a122d2f6bed34ddd9570b98591d2cbc3.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
