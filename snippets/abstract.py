import base64
# import collections

def apply_args_to_obj(obj, nn, *aa, **kk):
	tail_count = len(nn) - len(aa)
	aa += (None, ) * tail_count
	# dd = collections.OrderedDict(zip(nn, aa))
	dd = dict(zip(nn, aa))
	dd.update(kk)
	# obj.__dict__ = dd
	obj.__dict__.update(dd)

def NamedTuple(keys):

	def _(cls):
		setattr(cls, "__init__", lambda self, *aa, **kk: apply_args_to_obj(self, keys.split(), *aa, **kk))
		setattr(cls, "__str__", lambda self: self.__class__.__name__ + str(self.__dict__))
		setattr(cls, "__cmp__", lambda self, obj: cmp(self.to_tuple(), obj.to_tuple()))
		setattr(cls, "to_tuple", lambda self: tuple((self.__dict__[key] for key in keys.split())))
		setattr(cls, "from_obj", classmethod(lambda cls, obj: cls(*obj.to_tuple())))
		return cls
	return _

def SignatureDict(keys=None):
	def _(cls):
		setattr(cls, "get_signature_dict", lambda self: {key : self.__dict__[key] for key in keys.split()} if isinstance(keys, str) else self.__dict__)
		setattr(cls, "__repr__", lambda self: self.__class__.__name__ + str(self.get_signature_dict()))
		return cls
	return _

def Pickleable(ext=".pickle", keys=None):
	def _(cls):
		setattr(cls, "get_pickleable_name", lambda self: base64.b64encode(unicode(self.get_signature_dict()), "+-"))
		setattr(cls, "derive_pickle_path", lambda self: self.get_pickleable_name() + ext)
		if not hasattr(cls, "get_signature_dict"):
			return SignatureDict(keys)(cls)
		return cls
	return _
