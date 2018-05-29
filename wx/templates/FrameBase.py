import wx

from dejan7.wx.Accels import *
from dejan7.wx.helpers.StatusBarTimeoutHelper import *
from dejan7.wx.mixins.NoEraseBackgroundMixin import *


class FrameBase(wx.Frame):

	def __init__(self, title=__file__, size=(400,300)):
		wx.Frame.__init__(self, None, title=title, size=size)
		NoEraseBackgroundMixin(self)

		self.SetExtraStyle(wx.WS_EX_PROCESS_UI_UPDATES)
		self.SetFont(wx.FFont(14, wx.MODERN))

		self.status_info_timeout_action = None
		self.status_bar_timeout_helper = StatusBarTimeoutHelper(self)

	def ShowCentered(self):
		self.Center()
		self.Show()

	def SetStatusMessage(self, msg, timeout=0):
		if self.status_info_timeout_action:
			self.status_info_timeout_action.Clear()
			self.status_info_timeout_action = None

		self.status_info_timeout_action = self.status_bar_timeout_helper.SetStatusText(msg, timeout=timeout)

	def SetAccels(self, args_dicts):
		acc = Accels()
		for args_dict in args_dicts:
			acc.Add(**args_dict)
		acc.Install(self)

	def BindToUpdateUi(self, on=True, callback=None):
		if on: self.Bind(wx.EVT_UPDATE_UI, callback if callback else self.OnUpdateUi)
		else: self.Unbind(wx.EVT_UPDATE_UI)

	def OnUpdateUi(self, e):
		print __file__, "| OnUpdateUi |", e
