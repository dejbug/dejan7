import wx

class SimpleSizer(wx.BoxSizer):

	def __init__(self, first, second, gap=0, leftHeavy=False, rightHeavy=False, topHeavy=False, bottomHeavy=False):

		self.first = first
		self.second = second

		horizontal = leftHeavy or rightHeavy
		vertical = topHeavy or bottomHeavy

		assert horizontal or vertical
		assert not (horizontal and vertical)

		firstHeavy = leftHeavy or topHeavy
		secondHeavy = rightHeavy or bottomHeavy

		wx.BoxSizer.__init__(self, wx.VERTICAL if vertical else wx.HORIZONTAL)
		if first: self.Add(first, 1 if firstHeavy else 0, wx.EXPAND)
		if gap: self.AddSpacer(gap)
		if second: self.Add(second, 1 if secondHeavy else 0, wx.EXPAND)

	@classmethod
	def new(cls, code, *aa, **kk):

		assert 4 == len(code)
		assert code[0] in "LRTB"
		assert code[1] in "HRB"
		assert code[2] in "VH"
		assert code[3] in "VH"

		s = cls(*aa, leftHeavy="L" == code[0], rightHeavy="R" == code[0], topHeavy="T" == code[0] or "T" == code[1], bottomHeavy="B" == code[0] or "B" == code[1], **kk)

		if not "V" == code[2]: s.SetFirstVisible(False)
		if not "V" == code[3]: s.SetSecondVisible(False)

		return s

	def Install(self, parent):
		parent.SetSizer(self)

	def GetFirst(self):
		# return self.GetItem(0).GetWindow()
		return self.first

	def GetSecond(self):
		# return self.GetItem(1).GetWindow()
		return self.second

	def IsFirstVisible(self):
		return self.IsShown(0)

	def IsSecondVisible(self):
		return self.IsShown(1)

	def SetFirstVisible(self, on=True, recursive=False, refresh=True):
		if on: self.Show(0, recursive=recursive)
		else: self.Hide(0, recursive=recursive)
		if refresh: self.Layout()

	def SetSecondVisible(self, on=True, recursive=False, refresh=True):
		if on: self.Show(1, recursive=recursive)
		else: self.Hide(1, recursive=recursive)
		if refresh: self.Layout()

	def ToggleFirstVisible(self, recursive=False, refresh=True):
		self.SetFirstVisible(not self.IsFirstVisible(), recursive, refresh)

	def ToggleSecondVisible(self, recursive=False, refresh=True):
		self.SetSecondVisible(not self.IsSecondVisible(), recursive, refresh)

	def ToggleVisible(self, recursive=False, refresh=True):
		self.SetFirstVisible(not self.IsFirstVisible(), recursive, refresh)
		self.SetSecondVisible(not self.IsSecondVisible(), recursive, refresh)
		self.Layout()
