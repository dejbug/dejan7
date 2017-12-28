import wx

class SimpleSizer(wx.BoxSizer):

	def __init__(self, first, last, gap=0, bottomHeavy=None, rightHeavy=None):
		vertical = bottomHeavy is not None
		horizontal = rightHeavy is not None

		assert vertical or horizontal
		assert not (vertical and horizontal)

		lastHeavy = bottomHeavy or rightHeavy

		wx.BoxSizer.__init__(self, wx.VERTICAL if vertical else wx.HORIZONTAL)
		if first: self.Add(first, 0 if lastHeavy else 1, wx.EXPAND)
		if gap: self.AddSpacer(gap)
		if last: self.Add(last, 1 if lastHeavy else 0, wx.EXPAND)

	def Install(self, parent):
		parent.SetSizer(self)

	def IsFirstVisible(self):
		return self.IsShown(0)

	def IsLastVisible(self):
		return self.IsShown(1)

	def SetFirstVisible(self, on=True):
		if on: self.Show(0, recursive=True)
		else: self.Hide(0, recursive=True)
		self.Layout()

	def SetLastVisible(self, on=True):
		if on: self.Show(1, recursive=True)
		else: self.Hide(1, recursive=True)
		self.Layout()

	def ToggleFirstVisible(self):
		self.SetFirstVisible(not self.IsFirstVisible())

	def ToggleLastVisible(self):
		self.SetLastVisible(not self.IsLastVisible())
