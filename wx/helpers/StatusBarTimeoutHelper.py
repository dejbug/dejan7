import wx
import threading

class StatusBarTimeoutHelper(object):

	class TimeoutAction(object):

		def __init__(self, parent, action_id):
			self.parent = parent
			self.action_id = action_id

		def Clear(self, text=None, number=0):
			self.Cancel("", number)

		def Cancel(self, text=None, number=0):
			if self.action_id == self.parent.last_action_id:
				self.parent.Cancel(text, number)
				self.action_id = None
				return True
			return False

	def __init__(self, parent):
		self.parent = parent
		self.thread_mutex = threading.RLock()
		self.thread = None
		self.last_action_id = 0

	def Clear(self, number=0):
		self.CancelTimeout()
		self.SetFrameStatusText(self.parent, "", 0)

	def Cancel(self, text=None, number=0):
		self.CancelTimeout()
		if text is not None:
			if number is not None:
				self.SetFrameStatusText(self.parent, text, number)

	def SetStatusText(self, text, number=0, timeout=0):
		self.SetFrameStatusText(self.parent, text, number)
		return self.SetTimeout(number, timeout)

	def CancelTimeout(self):
		with self.thread_mutex:
			if self.thread:
				self.thread.cancel()
				self.thread = None

	def SetTimeout(self, number, timeout):
		with self.thread_mutex:
			if self.thread:
				self.thread.cancel()
				self.thread = None

			if not timeout: return None

			self.thread = threading.Timer(timeout, self.OnTimeout, args=[number])
			self.thread.daemon = True
			self.thread.start()

			self.last_action_id += 1
			return self.TimeoutAction(self, self.last_action_id)

	def OnTimeout(self, number):
		self.thread = None
		self.SetFrameStatusText(self.parent, "", 0)

	@classmethod
	def SetFrameStatusText(cls, frame, text="", number=0):
		try: frame.SetStatusText(text, number)
		except wx.PyDeadObjectError: pass
