# import pprint

class ToString(object):

	# PFORMAT_DEPTH = None
	UNDEFINED_STRING = "<undefined>"

	def __init__(self, keys=None):
		if keys and not isinstance(keys, str): raise TypeError("ToString: 1st argument 'keys' must be a string (or None); did you mean to write @ToString() ?")

		self.keys = keys.split() if isinstance(keys, str) else []

	def __call__(self, cls):
		setattr(cls, "to_string", lambda obj: type(obj).__name__ + (self.get_keyed_dict(obj) if self.keys else str(obj.__dict__)))

		# setattr(cls, "__str__", lambda obj: obj.to_string())
		setattr(cls, "__repr__", lambda obj: obj.to_string())

		return cls

	def get_keyed_dict(self, obj):
		# dd = {k:None for k in self.keys}
		# dd.update(obj.__dict__)

		ss = ("%s=%s" % (k, (self.pformat(obj.__dict__[k]) if k in obj.__dict__ else UNDEFINED_STRING)) for k in self.keys)
		return "[%s]" % ", ".join(ss)

	@classmethod
	def pformat(cls, val):
		# return pprint.pformat(val, depth=cls.PFORMAT_DEPTH)
		return repr(val)
