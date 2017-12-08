import wx

from TextCenteringHelper import *

class VirtualHelper(object):

	def __init__(self, cy=42):
		self.cy = cy
		self.fonts = [
			wx.FFontFromPixelSize(wx.Size(0, cy*.6), wx.TELETYPE),
			wx.FFontFromPixelSize(wx.Size(0, cy), wx.SWISS)]

	def AddFontFromSize(self, size, family=wx.SWISS):
		kk = {}
		if isinstance(family, int):
			kk["family"] = family
		elif isinstance(family, (str, unicode)):
			kk["family"] = wx.FONTFAMILY_DEFAULT
			kk["face"] = family

		self.fonts.append(wx.FFontFromPixelSize(size, **kk))

	def AddFontFromPoints(self, points, family=wx.SWISS):
		kk = {}
		if isinstance(family, int):
			kk["family"] = family
		elif isinstance(family, (str, unicode)):
			kk["family"] = wx.FONTFAMILY_DEFAULT
			kk["faceName"] = family

		self.fonts.append(wx.FFont(points, **kk))

	def AddFontFromHeight(self, height, family=wx.SWISS):
		kk = {}
		if isinstance(family, int):
			kk["family"] = family
		elif isinstance(family, (str, unicode)):
			kk["family"] = wx.FONTFAMILY_DEFAULT
			kk["face"] = family

		self.fonts.append(wx.FFontFromPixelSize((0, height), **kk))

	def GetPartialTextSimple(self, dc, text, maxWidth, fontId=0):
		dc.SetFont(self.fonts[fontId])
		averageCharWidth = dc.GetCharWidth()
		maxCharCount = maxWidth / averageCharWidth
		if len(text) <= maxCharCount:
			return text
		return text[:maxCharCount-2] + "..."

	def GetPartialText(self, dc, text, maxWidth, fontId=0):
		dc.SetFont(self.fonts[fontId])
		partialExtents = dc.GetPartialTextExtents(text)

		if partialExtents[-1] < maxWidth:
			return text

		ellipsisWidth, ellipsisHeight = dc.GetTextExtent("...")

		maxCharCount = 0
		for w in partialExtents:
			if w < maxWidth-ellipsisWidth:
				maxCharCount += 1
			else: break
		if len(text) <= maxCharCount:
			return text
		return text[:maxCharCount] + "..."

	def GetTextExtent(self, dc, text, fontId=0):
		dc.SetFont(self.fonts[fontId])
		return dc.GetTextExtent(text)

	def GetCenterOffset(self, dc, rc, text, fontId=0):
		tw, th = self.GetTextExtent(dc, text, fontId)
		return (rc.width - tw) / 2

	def DrawString(self, dc, r, text, fontId=0, xoff=2, color="black"):
		dc.SetFont(self.fonts[fontId])
		dc.SetTextForeground(color)
		tch = TextCenteringHelper(dc, r, text)
		dc.DrawText(text, r.x+xoff, r.y+tch.y)
		return tch.w+xoff
