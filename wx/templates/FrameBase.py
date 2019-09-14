import os, os.path
import sys

import wx

from dejan7.wx.Accels import *
from dejan7.wx.helpers.StatusBarTimeoutHelper import *
from dejan7.wx.mixins.NoEraseBackgroundMixin import *


class FrameBase(wx.Frame):

	def __init__(self, title=sys.argv[0], size=(400,300), no_erase_background=True):
		wx.Frame.__init__(self, None, title=title, size=size)
		NoEraseBackgroundMixin(self)

		self.SetExtraStyle(wx.WS_EX_PROCESS_UI_UPDATES)
		self.SetFont(wx.FFont(14, wx.MODERN))

		self.user_passed_title = title
		
		self.status_info_timeout_action = None
		self.status_bar_timeout_helper = StatusBarTimeoutHelper(self)

	def FindAndLoadIcons(self):

		app_icon_name = wx.GetApp().GetAppName() + ".ico"
		app_icon_path = ""

		sp = wx.StandardPaths.Get()

		search_paths = (
			".",
			sp.GetExecutablePath(),
			sp.GetDataDir(),
		)

		for search_path in search_paths:
			p = os.path.join(search_path, app_icon_name)
			if os.path.isfile(p):
				app_icon_path = p
				break

		if app_icon_path:
			ib = wx.IconBundle()
			ib.AddIconFromFile(app_icon_path, wx.BITMAP_TYPE_ANY)
			self.SetIcons(ib)

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
