import wx

from dejan7.wx.PopupStatusBar import *
from dejan7.wx.helpers.TimeoutHelper import *


class StatusBarTimeoutHelper(object):

	def __init__(self, parent):
		self.parent = parent

		self.popup_status_bar = PopupStatusBar(parent)

		self.timeout_helper = TimeoutHelper()
		self.timeout_helper.Subscribe("cancel", self.OnTimeoutHelperCancel)
		self.timeout_helper.Subscribe("timeout", self.OnTimeoutHelperTimeout)

	def OnTimeoutHelperCancel(self, source, action):
		try:
			self.popup_status_bar.SetText("cancel", 0)
			self.popup_status_bar.Hide()
		except wx.PyDeadObjectError: pass

	def OnTimeoutHelperTimeout(self, source, action):
		try:
			self.popup_status_bar.SetText("timeout", 0)
			self.popup_status_bar.Hide()
		except wx.PyDeadObjectError: pass

	def SetStatusText(self, text, number=0, timeout=0):
		self.popup_status_bar.Show()
		self.popup_status_bar.SetText(text, number)
		return self.timeout_helper.Set(timeout, text=text, number=number)
