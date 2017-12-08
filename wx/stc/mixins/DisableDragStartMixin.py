import time

import wx
import wx.stc

class DisableDragStartMixin(object):

	def __init__(self, parent):
		self.parent = parent
		self.selectionCleared = False
		self.newCurPos = 0
		self.dclickMsec = wx.SystemSettings.GetMetric(wx.SYS_DCLICK_MSEC)
		self.lastTime = time.time()
		self.parent.Bind(wx.stc.EVT_STC_START_DRAG, self.OnStcStartDrag)
		self.parent.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
		self.parent.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDclick)

	def OnStcStartDrag(self, e):
		e.Skip()
		e.SetDragText("")

	def OnLeftDown(self, e):
		e.Skip()

		self.newCurPos = self.parent.PositionFromPoint(e.GetPosition())

		if self.newCurPos >= self.parent.GetSelectionNStart(0) and self.newCurPos <= self.parent.GetSelectionNEnd(0):
			self.parent.GotoPos(self.newCurPos)
			self.selectionCleared = True
			self.lastTime = time.time()
		else:
			self.selectionCleared = False

	def OnLeftDclick(self, e):
		# self.dclickMsec = wx.SystemSettings.GetMetric(wx.SYS_DCLICK_MSEC)
		deltaMsec = int((time.time() - self.lastTime) * 1000)

		if deltaMsec > self.dclickMsec and self.selectionCleared:
			self.selectionCleared = False
			# self.newCurPos = self.parent.PositionFromPoint(e.GetPosition())
			if self.newCurPos != self.parent.WordStartPosition(self.newCurPos, True):
				self.parent.WordLeft()
			self.parent.WordPartRightExtend()
		else:
			e.Skip()
