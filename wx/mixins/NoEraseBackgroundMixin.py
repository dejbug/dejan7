import wx

class NoEraseBackgroundMixin(object):

	def __init__(self, parent):
		self.parent = parent
		self.parent.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

	def OnEraseBackground(self, e):
		self.parent.SetBackgroundStyle(wx.BG_STYLE_PAINT)
