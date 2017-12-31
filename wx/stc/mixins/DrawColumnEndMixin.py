import wx
import wx.stc

from dejan7.async.DelayedCall import *
from dejan7.wx.stc import GetRowWidths

class DrawColumnEndMixin(object):

	def __init__(self, parent, color="GREY", delay=0.3, margins=[]):
		self.sci = parent
		self.pen = wx.Pen(color)
		self.margins = margins

		self.DelayedPaint = DelayedCall(self.Paint, delay)

		PaintMethod = self.OnPaintedDelayed if delay > 0 else self.OnPainted
		self.sci.Bind(wx.stc.EVT_STC_PAINTED, PaintMethod)

	def OnPaintedDelayed(self, e):
		e.Skip()
		self.DelayedPaint()

	def OnPainted(self, e):
		e.Skip()
		self.Paint()

	def Paint(self):
		th = self.sci.TextHeight(0)

		dc = wx.ClientDC(self.sci)
		wx.DCPenChanger(dc, self.pen)

		y = 0
		for x in GetRowWidths(self.sci, margins=self.margins):
			if x >= 0: dc.DrawLine(x, y, x, y + th)
			y += th
