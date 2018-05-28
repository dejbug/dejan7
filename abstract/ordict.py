import collections

class ordict(collections.OrderedDict):

	def __repr__(self):
		return type(self).__name__ + "[" + ", ".join(list("%s=%s" % (k, repr(v)) for k,v in zip(self.keys(), self.values()))) + "]"

	def __setattr__(self, key, value):
		if key in ("_OrderedDict__root", "_OrderedDict__map"):
			return super(ordict, self).__setattr__(key, value)
		self[key] = value
		return value

	def __getattr__(self, key):
		if key in ("_OrderedDict__root", "_OrderedDict__map"):
			return super(ordict, self).__getattr__(key)
		elif key in self.keys():
			return self[key]
		else:
			self[key] = None
			return None
