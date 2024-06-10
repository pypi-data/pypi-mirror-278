
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'LocalPipeline_1e40e33515dc43e68d28af60b39b0c94.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
