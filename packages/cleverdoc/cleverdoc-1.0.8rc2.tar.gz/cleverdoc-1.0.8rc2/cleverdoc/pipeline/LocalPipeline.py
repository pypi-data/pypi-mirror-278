
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'LocalPipeline_af797e98dd3e42e3b7994fd7fe54af5f.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
