# import wx.stc

def PrintLexerProperties(scintillaEditor):
	print scintillaEditor.PropertyNames()
	for name in scintillaEditor.PropertyNames().split():
		print "-" * 78
		print name
		print scintillaEditor.DescribeProperty(name)

class SettingsApplier(object):

	def SetFontFromSettings(self, *aa, **kk): pass
	def SetForegroundFromSettings(self, *aa, **kk): pass
	def SetBackgroundFromSettings(self, *aa, **kk): pass
