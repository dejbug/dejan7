def strfromdict(cls):
	setattr(cls, "__str__", lambda obj: obj.__class__.__name__ + str(obj.__dict__))
	return cls
