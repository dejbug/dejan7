import cPickle as pickle
import os
import re
import zipfile

DEFAULT_PATH = "store.zip"

class Store(object):

	class Error(Exception): pass
	class NotOpenError(Error): pass
	class OverwriteError(Error): pass

	def __init__(self, path=DEFAULT_PATH):
		self.path = path
		self.file = None

	def __iter__(self):
		return self.enum()

	def __enter__(self):
		return self.open()

	def __exit__(self, x, m, t):
		self.close()

	def open(self):
		self.file = zipfile.ZipFile(self.path, "a", compression=zipfile.ZIP_DEFLATED)
		return self

	def close(self):
		if self.file:
			self.file.close()
			self.file = None

	def add(self, path_or_pickleable, data=None, force=False):
		if not self.file: raise self.NotOpenError("Store::add: can't write to Store: Store not open yet for business")

		if hasattr(path_or_pickleable, "derive_pickle_path"):
			path = path_or_pickleable.derive_pickle_path()
			if data is None: data = path_or_pickleable
		else:
			path = path_or_pickleable
			# if data is None: raise ValueError("Store::add: 2nd argument 'data' is None")

		try: extant_info = self.file.getinfo(path)
		except KeyError: extant_info = None

		zip_date_to_str = lambda d: "%d-%d-%d-%02d:%02d:%02d" % d

		if not force and extant_info: raise self.OverwriteError("Store::add: path already exists at '%s' and force flag was not specified: ZipInfo{date: %s size: %d (%d) crc: %d}" % (path, zip_date_to_str(extant_info.date_time), extant_info.file_size, extant_info.compress_size, extant_info.CRC))

		self.file.writestr(path, pickle.dumps(data, pickle.HIGHEST_PROTOCOL))

	def get(self, path_or_pickleable):
		if not self.file: raise self.NotOpenError("Store::get: can't write to Store: Store not open yet for business")

		if hasattr(path_or_pickleable, "derive_pickle_path"):
			path = path_or_pickleable.derive_pickle_path()
		else:
			path = path_or_pickleable

		return pickle.loads(self.file.read(path))

	def enum(self, ext=None, case_sensitive=False):
		if ext:
			ext_ = ext.lower() if ext else None
			has_ext_s = lambda p: p.endswith(ext) if ext else True
			has_ext_i = lambda p: p.lower().endswith(ext_) if ext_ else True
			has_ext = has_ext_s if case_sensitive else has_ext_i
			pp = (p for p in self.file.namelist() if has_ext(p))
		else:
			pp = (p for p in self.file.namelist())
		return iter(pp)
