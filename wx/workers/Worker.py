import threading

import wx


class Worker(wx.EvtHandler):

	def __init__(self, done_cb, run_cb=None, timer_freq=10):
		wx.EvtHandler.__init__(self)

		self.done_cb = done_cb
		assert hasattr(done_cb, "__call__")

		self.run_cb = run_cb or self.Main
		self.result = None

		self.timer_freq = timer_freq

		self.ready = threading.Event()
		self.ready.set()

		self.worker = None
		self.timer = wx.Timer(self)

		self.Bind(wx.EVT_TIMER, self.OnTimer)

	def Main(self, path):
		"""Override this, if no run_cb callback passed to ctor.
		Do all work here and return result(s)."""
		return None

	def Start(self, *aa, **kk):
		self.ready.wait()

		self.worker = threading.Thread(target=self._run, args=aa, kwargs=kk)
		self.worker.daemon = True
		self.worker.start()

		self.timer.Start(self.timer_freq)

	def _run(self, *aa, **kk):
		self.result = self.run_cb(*aa, **kk)

	def OnTimer(self, e):

		if self.worker:
			self.worker.join()

		self.worker = None
		self.ready.set()
		self.timer.Stop()

		self.done_cb(self.result)
