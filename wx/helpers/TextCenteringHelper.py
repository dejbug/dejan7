import wx

class TextCenteringHelper(object):
	def __init__(self, dc, r, text):
		assert isinstance(r, wx.Rect)
		self.w, self.h = dc.GetTextExtent(text)
		self.x, self.y = (r.width-self.w)>>1, (r.height-self.h)>>1

	@classmethod
	def GetTextCenteringOffsets(cls, dc, r, text):
		w, h = dc.GetTextExtent(text)
		return (r.width-w)>>1, (r.height-h)>>1
