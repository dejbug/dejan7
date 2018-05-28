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

		assert 3 == len(code)
		
		# "heaviness" : Left, Right, Top, Bottom,
		#	Vertical (Top + Bottom), or
		#	Horizontal (Left + Right)
		assert code[0] in "LRTBVH"
		
		# "visibility": visible or hidden
		assert code[1] in "VH" # 1st visible or hidden
		assert code[2] in "VH" # 2nd visible or hidden

		s = cls(*aa,
			leftHeavy=(code[0] in "LH"),
			rightHeavy=(code[0] in "RH"),
			topHeavy=(code[0] in "TV"),
			bottomHeavy=(code[0] in "BV"),
			**kk)

		if not "V" == code[1]: s.SetFirstVisible(False)
		if not "V" == code[2]: s.SetSecondVisible(False)

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
		if on: self.GetFirst().SetFocus()
		if refresh: self.Layout()

	def SetSecondVisible(self, on=True, recursive=False, refresh=True):
		if on: self.Show(1, recursive=recursive)
		else: self.Hide(1, recursive=recursive)
		if on: self.GetSecond().SetFocus()
		if refresh: self.Layout()

	def ToggleFirstVisible(self, recursive=False, refresh=True):
		self.SetFirstVisible(not self.IsFirstVisible(), recursive, refresh)

	def ToggleSecondVisible(self, recursive=False, refresh=True):
		self.SetSecondVisible(not self.IsSecondVisible(), recursive, refresh)

	def ToggleVisible(self, recursive=False):
		self.SetFirstVisible(not self.IsFirstVisible(), recursive, False)
		self.SetSecondVisible(not self.IsSecondVisible(), recursive, False)
		self.Layout()
		