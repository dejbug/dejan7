from dejan7.storage.Pickler import Pickler

from Pickleable1 import *

def Pickleable2(ext=".pickle", keys=None):
	def _(cls):
		setattr(cls, "unpickle_from_file", lambda self, file: Pickler.load_from_file(file))
		setattr(cls, "unpickle_from_path", lambda self, path: Pickler.load_from_path(self.derive_pickle_path()))
		setattr(cls, "pickle_to_file", lambda self, file: Pickler.save_to_file(file, self))
		setattr(cls, "pickle_to_path", lambda self, path: Pickler.save_to_path(self.derive_pickle_path(), self))
		if not hasattr(cls, "derive_pickle_path"):
			return Pickleable1(ext, keys)(cls)
		return cls
	return _
