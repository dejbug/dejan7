import math

import wx.stc

class LineNumberMarginHelper(object):

	def __init__(self, sci):
		self.sci = sci

	def Update(self, event):
		if event.GetLinesAdded():
			self.UpdateLineNumberMarginWidth()

	def UpdateLineNumberMarginWidth(self):
		self.SetMarginWidthByDigitsCount(self.sci, self.GetDigitCount())

	def GetDigitCount(self, lineCount=-1):
		return self.CountDigits(lineCount if lineCount < 0 else self.sci.GetLineCount())

	@classmethod
	def SetMarginWidthByDigitsCount(cls, sci, digitsCount, marginIndex=0):
		return sci.SetMarginWidth(marginIndex, sci.TextWidth(wx.stc.STC_STYLE_LINENUMBER, "_" + "9" * digitsCount))

	@classmethod
	def CountDigits(cls, value):
		return 1 + int(math.log(abs(value), 10)) + (1 if value < 0 else 0)
