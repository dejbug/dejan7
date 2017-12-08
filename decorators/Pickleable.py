import base64

from SignatureDict import *

def Pickleable(ext=".pickle", keys=None):
	def _(cls):
		setattr(cls, "get_pickleable_name", lambda self: base64.b64encode(unicode(self.get_signature_dict()), "+-"))
		setattr(cls, "derive_pickle_path", lambda self: self.get_pickleable_name() + ext)
		if not hasattr(cls, "get_signature_dict"):
			return SignatureDict(keys)(cls)
		return cls
	return _
