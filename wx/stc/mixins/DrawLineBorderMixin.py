import wx
import wx.stc

from dejan7.async.DelayedCall import *
from dejan7.wx.stc import GetLastWrappedRowsY

class DrawLineBorderMixin(object):

	def __init__(self, parent, color="GREY", delay=0.3):
		self.sci = parent
		self.pen = wx.Pen(color)

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
		## TODO: It flickers. In the C++ version I used clipping to
		## reduce it, but it has to happen before Scintilla draws
		## itself. Maybe we can do a double buffer here? We would
		## have to blit the client to our MemoryDC,then draw our
		## stuff on top of it, then blit it back. Seems unelegant
		## but, if it works, why not?

		s = self.sci.GetClientSize()

		dc = wx.ClientDC(self.sci)
		wx.DCPenChanger(dc, self.pen)

		for y in GetLastWrappedRowsY(self.sci):
			dc.DrawLine(0, y, s.width, y)
