import pickle

from dejan7.storage.Store import Store

class StoreHelper(object):

	class Error(Exception): pass
	class KeyError(Error): pass
	class IndexError(Error): pass

	@classmethod
	def get_store_object_by_index(cls, index, ext=None, case_sensitive=False, store_aa=[], store_kk={}):
		if index < 0: raise IndexError("StoreHelper.get_store_object_by_index: 1st argument 'index' (%d) must be non-negative" % index)
		with Store(*store_aa, **store_kk) as store:
			paths = tuple(store.enum(ext, case_sensitive))
			if index > len(paths): raise IndexError("1st argument 'index' (%d) is out of bounds: item count is %d" % (index, len(paths)))
			path = paths[long(index)]
			return store.get(path)

	@classmethod
	def dump_store_object_by_index(cls, file, index, key="", ext=None, case_sensitive=False, store_aa=[], store_kk={}):
		if key and not isinstance(key, str): raise KeyError("3rd argument 'key' must be a string (or None)")
		obj = cls.get_store_object_by_index(index, ext, case_sensitive, *store_aa, **store_kk)
		if not key: file.write(obj)
		else:
			if not hasattr(obj, key): raise KeyError("3rd argument 'key' (%s) is not a valid attribute of object '%s'" % (key, repr(obj)))
			data = getattr(obj, key)
			pickle.dump(data, file)
