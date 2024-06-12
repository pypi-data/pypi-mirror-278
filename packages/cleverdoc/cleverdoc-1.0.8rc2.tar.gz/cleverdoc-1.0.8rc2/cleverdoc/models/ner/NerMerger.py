
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'NerMerger_616bfd57c7054586bb47e447c1c104b5.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
