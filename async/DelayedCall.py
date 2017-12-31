import threading
import traceback

class DelayedCall(object):

	def __init__(self, target, seconds=0.0):
		self.target = target
		self.seconds = seconds
		self.timer = None

	def run(self, *aa, **kk):
		try: self.target(*aa, **kk)
		# except wx.PyDeadObjectError: pass
		except Exception as e:
			if "PyDeadObjectError" == type(e).__name__: pass
			else: traceback.print_exc()

	def __call__(self, *aa, **kk):
		if self.timer:
			self.timer.cancel()
			self.timer = None

		if self.seconds > 0:
			self.timer = threading.Timer(self.seconds, self.run, args=aa, kwargs=kk)
			self.timer.start()
		else:
			self.run(*aa, **kk)
