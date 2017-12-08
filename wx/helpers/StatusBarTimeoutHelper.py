import threading

class StatusBarTimeoutHelper(object):

	def __init__(self, parent):
		self.parent = parent
		self.thread_mutex = threading.RLock()
		self.thread = None

	def SetStatusText(self, text, number=0, timeout=0):
		self.parent.SetStatusText(text, number)
		self.SetTimeout(number, timeout)

	def SetTimeout(self, number, timeout):
		with self.thread_mutex:
			with self.thread_mutex:
				if self.thread:
					self.thread.cancel()
					self.thread = None

			if not timeout: return

			self.thread = threading.Timer(timeout, self.OnTimeout, args=[number])
			self.thread.start()

	def OnTimeout(self, number):
		self.thread = None
		self.parent.SetStatusText("", number)
