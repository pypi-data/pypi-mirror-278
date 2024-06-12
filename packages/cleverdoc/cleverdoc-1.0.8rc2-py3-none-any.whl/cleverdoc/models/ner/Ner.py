
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Ner_6e3bc231cec84db9b522525567ca3944.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
