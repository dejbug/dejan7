from dejan7.helpers import apply_args_to_obj

def NamedTuple(keys):

	def _(cls):
		setattr(cls, "__init__", lambda self, *aa, **kk: apply_args_to_obj(self, keys.split(), *aa, **kk))
		setattr(cls, "__str__", lambda self: self.__class__.__name__ + str(self.__dict__))
		setattr(cls, "__cmp__", lambda self, obj: cmp(self.to_tuple(), obj.to_tuple()))
		setattr(cls, "to_tuple", lambda self: tuple((self.__dict__[key] for key in keys.split())))
		setattr(cls, "from_obj", classmethod(lambda cls, obj: cls(*obj.to_tuple())))
		return cls
	return _
