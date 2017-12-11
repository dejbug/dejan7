import wx

class Menu(wx.MenuBar):

	def __init__(self, parent, base_id=1000):
		wx.MenuBar.__init__(self)
		self.parent = parent
		parent.SetMenuBar(self)
		self.current = None
		self.base_id = base_id

	def GetNextId(self):
		self.base_id += 1
		return self.base_id

	def GetCurrentSubmenu(self):
		return self.current

	def AppendMenu(self, label):
		self.current = wx.Menu()
		self.Append(self.current, label)

	def AppendItem(self, label, id=None, help="", callback=None):
		id = id or self.GetNextId()
		self.current.Append(id, label, help)
		if callback:
			self.parent.Bind(wx.EVT_MENU, callback, id=id)

	def AppendCheckItem(self, label, id=None, help="", callback=None):
		id = id or self.GetNextId()
		self.current.AppendCheckItem(id, label, help)
		if callback:
			self.parent.Bind(wx.EVT_MENU, callback, id=id)

	def AppendSubMenu(self, label):
		pass

	def AppendSeparator(self):
		self.current.AppendSeparator()
