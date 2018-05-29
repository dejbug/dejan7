import wx

from dejan7.wx.helpers.TextCtrlHelper import *


def TextCtrlLineDragDecorator(decorated):

	def OnMiddleDown(self, e):
		self.hit_y = self.ctrl.GetRowIndexUnderCursor()
		self.CaptureMouse()
		self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
		e.Skip()

	def OnMiddleUp(self, e):
		self.hit_y = None
		if self.HasCapture():
			self.ReleaseMouse()
		self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
		e.Skip()

	def OnMotion(self, e):
		if None != self.hit_y:
			row_index_under_cursor = self.ctrl.GetRowIndexUnderCursor()
			if None == row_index_under_cursor: return
			direction = self.hit_y - row_index_under_cursor
			self.ctrl.ScrollLines(direction)
		e.Skip()

	def Enable(self):
		self.ctrl = TextCtrlHelper(self)
		self.hit_y = None
		self.Bind(wx.EVT_MIDDLE_DCLICK, self.TextCtrlLineDragDecorator_OnMiddleDown)
		self.Bind(wx.EVT_MIDDLE_DOWN, self.TextCtrlLineDragDecorator_OnMiddleDown)
		self.Bind(wx.EVT_MIDDLE_UP, self.TextCtrlLineDragDecorator_OnMiddleUp)
		self.Bind(wx.EVT_MOTION, self.TextCtrlLineDragDecorator_OnMotion)

	setattr(decorated, "TextCtrlLineDragDecorator_OnMiddleDown", OnMiddleDown)
	setattr(decorated, "TextCtrlLineDragDecorator_OnMiddleUp", OnMiddleUp)
	setattr(decorated, "TextCtrlLineDragDecorator_OnMotion", OnMotion)
	setattr(decorated, "EnableTextCtrlLineDragDecorator", Enable)

	return decorated
