import wx
# from wx.lib.pubsub import pub

from dejan7.helpers import zip_extend
from dejan7.wx.decorators.EventSource import *
from dejan7.wx.helpers.VirtualHelper import *

@EventSource("ItemActivate")
@EventSource("ItemSelect")
class SimpleVListBox(wx.VListBox):

	def __init__(self, parent, row_height=42):
		wx.VListBox.__init__(self, parent)
		self.vh = VirtualHelper(cy=row_height)
		self.items = []

		self.Bind(wx.EVT_LISTBOX, self.OnEvtListBox)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnEvtListBoxDClick)
		self.Bind(wx.EVT_MIDDLE_DOWN, self.OnEvtMiddleDown)

	def SetItems(self, items=[]):
		self.items = items
		self.SetItemCount(len(self.items))
		self.ScrollToRow(0)

	def CopyItemToClipboard(self, n, transform=unicode):
		try: it = self.items[n]
		except IndexError: return False
		tit = transform(it)
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(wx.TextDataObject(tit))
			wx.TheClipboard.Close()
			return True
		return False

	def SelectFromPoint(self, pos):
		n = self.HitTest(pos)
		self.SetSelection(n)
		return n

	def HandleItemActivated(self, n, method=None):
		self.PostItemActivateEvent(index=n, method=(method if method else "HandleItemActivated"))

	def HandleItemSelected(self, n, method=None):
		self.PostItemSelectEvent(index=n, method=(method if method else "HandleItemSelected"))

	def OnEvtListBox(self, e):
		e.Skip()
		self.HandleItemSelected(e.GetSelection(), method="OnEvtListBox")

	def OnEvtListBoxDClick(self, e):
		e.Skip()
		self.HandleItemActivated(e.GetSelection(), method="OnEvtListBoxDClick")

	def OnKeyDown(self, e):
		e.Skip()
		if e.GetKeyCode() == wx.VK_ENTER:
			self.HandleItemActivated(self, e.GetSelection(), method="OnKeyDown")

	def OnEvtMiddleDown(self, e):
		e.Skip()
		n = self.SelectFromPoint(e.GetPosition())
		self.HandleItemSelected(n, method="OnEvtMiddleDown")

	def OnMeasureItem(self, n):
		return self.vh.cy

	def OnDrawItem(self, dc, r, n):
		xoff = 16 + self.vh.DrawString(dc, r, "%3d" % (n+1), xoff=8)
		t = self.TextFromItem(n)
		if isinstance(t, list):
			for s, c, f, g in t:
				xoff = g + self.vh.DrawString(dc, r, s, f, xoff, c)
		else:
			xoff = self.vh.DrawString(dc, r, t, 1, xoff=xoff)

	def TextFromItem(self, n):
		return self.to_styled_text(["item #%d" % n, repr(self.items[n])], ["grey", "black"], [0, 1], [4, 8])

	@classmethod
	def to_styled_text(cls, text_parts, colors=[], font_ids=[], gaps=[]):
		return zip_extend(text_parts, ["black", 1, 4], colors, font_ids, gaps)
