import wx

class TabSwitcherMixin(object):

	def __init__(self, parent, next):
		self.next = next
		parent.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
	
	def OnKeyDown(self, e):
		if e.GetKeyCode() == wx.WXK_TAB:
			if self.next:
				self.next.SetFocus()
		else:
			e.Skip()
