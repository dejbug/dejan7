import wx

class ExitOnKeyMixin(object):

	def __init__(self, parent, key=wx.WXK_ESCAPE):
		self.key = key
		parent.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

	def OnKeyDown(self, e):
		if e.GetKeyCode() == self.key:
			wx.GetApp().GetTopWindow().Close()
		else:
			e.Skip()
