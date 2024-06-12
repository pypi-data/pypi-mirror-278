
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'NerLLM_1f8fc2ab67f94cc0826b29abb803b8d9.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
