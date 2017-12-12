import threading

class DelayedCall(object):

	def __init__(self, target, seconds=0.0):
		self.target = target
		self.seconds = seconds
		self.timer = None

	def __call__(self, *aa, **kk):
		if self.timer:
			self.timer.cancel()

		if self.seconds > 0:
			self.timer = threading.Timer(self.seconds, self.target, args=aa, kwargs=kk)
			self.timer.start()
		else:
			self.target(*aa, **kk)
