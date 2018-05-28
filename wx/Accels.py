import wx
from wx.lib.pubsub import pub

class Accels(wx.EvtHandler):

	ACCEL_BASE = 30000

	def __init__(self):
		wx.EvtHandler.__init__(self)
		self.last_id = self.ACCEL_BASE
		self.frame = None
		self.entries = []
		self.callbacks = []

	def Add(self, key, mod=wx.ACCEL_NORMAL, cb=None):
		if mod is None: mod = wx.ACCEL_NORMAL
		self.last_id += 1
		id = self.last_id
		self.entries.append(wx.AcceleratorEntry(mod, key, id))
		self.callbacks.append(cb)
		assert len(self.entries) == len(self.callbacks)

	def Install(self, frame):
		self.frame = frame
		accel = wx.AcceleratorTable(self.entries)
		self.frame.SetAcceleratorTable(accel)
		self.frame.Bind(wx.EVT_MENU, self._on_menu)

	def _on_menu(self, e):
		for entry, callback in zip(self.entries, self.callbacks):
			if entry.GetCommand() == e.GetInt():
				key = entry.GetKeyCode()
				mod = entry.GetFlags()
				if callback: callback(key=key, mod=mod)
				else: pub.sendMessage("accels", key=key, mod=mod)
				return True
		e.Skip()
		return False
