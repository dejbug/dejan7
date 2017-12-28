from contextlib import contextmanager

import wx

@contextmanager
def Freezer(obj):
	obj.Freeze()
	yield
	obj.Thaw()
