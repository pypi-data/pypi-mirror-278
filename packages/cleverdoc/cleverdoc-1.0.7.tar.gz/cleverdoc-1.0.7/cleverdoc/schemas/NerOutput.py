
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'NerOutput_a78effc8530e4738afa12bc7adec1545.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
