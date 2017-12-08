import math

import wx.stc

from dejan7.wx.stc.helpers.LineNumberMarginHelper import *

class LineNumberMarginAutoWidthMixin(object):

	def __init__(self, parent):
		self.helper = LineNumberMarginHelper(parent)
		parent.Bind(wx.stc.EVT_STC_MODIFIED, self.OnModified)

	def OnModified(self, event):
		self.helper.Update(event)
