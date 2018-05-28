import wx

class PopupStatusBar(wx.StatusBar):

	def __init__(self, parent, *aa, **kk):
		wx.StatusBar.__init__(self, parent)
		self.parent = parent
		self.is_popup_status_bar = None
		wx.StatusBar.Show(self, False)

	def Show(self):

		parent_has_statusbar = not not self.parent.GetStatusBar()
		self.is_popup_status_bar = not parent_has_statusbar

		if self.is_popup_status_bar:
			self.parent.SetStatusBar(self)
			wx.StatusBar.Show(self, True)

	def Hide(self):

		if self.is_popup_status_bar:
			self.parent.SetStatusBar(None)
			wx.StatusBar.Show(self, False)

			# self.parent.Layout()
			# self.parent.Refresh()
			self.parent.SendSizeEvent()

	def SetText(self, text="", number=0):

		parent_has_statusbar = not not self.parent.GetStatusBar()
		if parent_has_statusbar:
			self.parent.SetStatusText(text, number)
