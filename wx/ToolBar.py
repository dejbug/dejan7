import wx
import re

class ToolBar(wx.ToolBar):

	def __init__(self, parent, vertical=False):

		wx.ToolBar.__init__(self, parent, style=
			wx.TB_FLAT | (wx.TB_VERTICAL if vertical else 0)
		)

		self.parent = parent
		self.last_tool_id = 0

	def _default_calllback(self, e):
		print e

	def Install(self):
		self.Realize()
		self.parent.SetToolBar(self)

	def AddStandardTool(self, art_id=wx.ART_FILE_OPEN, callback=None):

		if not callback: callback = self._default_calllback

		self.last_tool_id += 1
		self.AddTool(self.last_tool_id, wx.ArtProvider.GetBitmap(art_id))
		self.Bind(wx.EVT_TOOL, callback, id=self.last_tool_id)

	def AddXpmTool(self, xpm_lines, callback=None):

		if not callback: callback = self._default_calllback

		if isinstance(xpm_lines, str):
			xpm_lines = re.split(r'[\r\n]+', xpm_lines)

		self.last_tool_id += 1
		self.AddTool(self.last_tool_id, bitmap=wx.BitmapFromXPMData(xpm_lines))
		self.Bind(wx.EVT_TOOL, callback, id=self.last_tool_id)
