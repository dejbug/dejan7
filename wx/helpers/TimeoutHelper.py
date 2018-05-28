import threading

from dejan7.wx.decorators.EventSource import EventSourcePS


@EventSourcePS
class TimeoutHelper(object):

	class TimeoutAction(object):

		def __init__(self, parent, action_id):
			self.parent = parent
			self.action_id = action_id

		def Cancel(self, *aa, **kk):
			if self.action_id == self.parent.last_action_id:
				self.parent.Cancel(*aa, **kk)
				self.action_id = None
				return True
			return False


	def __init__(self):
		self.thread_mutex = threading.RLock()
		self.thread = None
		self.last_action_id = 0

	def Set(self, timeout, *aa, **kk):

		if self.thread:
			with self.thread_mutex:
				self.thread.cancel()
				self.thread = None

		if not timeout: return None

		self.thread = threading.Timer(timeout, self._OnTimeout)
		self.thread.daemon = True
		self.thread.deamon = True
		self.thread.start()

		self.last_action_id += 1
		return self.TimeoutAction(self, self.last_action_id)

	def Cancel(self, *aa, **kk):
		if self.thread:
			with self.thread_mutex:
				self.thread.cancel()
				self.thread = None
			self.OnCancel(*aa, **kk)

	def _OnTimeout(self, *aa, **kk):
		self.thread = None
		self.OnTimeout(*aa, **kk)

	def OnCancel(self, *aa, **kk):
		self.PostEvent("cancel", source=self, action="cancel")

	def OnTimeout(self, *aa, **kk):
		self.PostEvent("timeout", source=self, action="timeout")
