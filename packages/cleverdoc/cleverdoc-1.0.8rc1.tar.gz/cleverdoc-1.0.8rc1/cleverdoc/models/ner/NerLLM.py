
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'NerLLM_839b09f7d3c54a5585262f09b5036613.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
