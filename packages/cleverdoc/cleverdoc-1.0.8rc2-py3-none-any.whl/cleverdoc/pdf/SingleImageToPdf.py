
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'SingleImageToPdf_1f24b6834c8f4addae939812a955e47f.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
