import wx


class FrameTitleHelper(object):

	def __init__(self):
		self.forms = []

	def Apply(self, frame, index):
		frame.SetTitle(self.Get(index))

	def Add(self, form, *aa):
		self.forms.append((form, aa))

	def Get(self, index):
		form = self.forms[index]
		args = self.MakeArgs(index)
		return form[0].format(*args)

	def MakeArgs(self, index):
		args = []
		for arg in self.forms[index][1]:
			if hasattr(arg, "__call__"):
				args.append(arg())
			else:
				args.append(arg)
		return args
