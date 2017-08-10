

import os


myo = os.popen('python3 genETHaddress.py').read()
print repr(myo)
