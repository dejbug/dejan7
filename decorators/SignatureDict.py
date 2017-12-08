
def SignatureDict(keys=None):
	def _(cls):
		setattr(cls, "get_signature_dict", lambda self: {key : self.__dict__[key] for key in keys.split()} if isinstance(keys, str) else self.__dict__)
		setattr(cls, "__repr__", lambda self: self.__class__.__name__ + str(self.get_signature_dict()))
		return cls
	return _
