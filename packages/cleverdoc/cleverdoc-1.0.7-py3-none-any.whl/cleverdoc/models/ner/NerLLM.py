
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'NerLLM_383d84c3d5a647d3a133c61b92d08128.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
