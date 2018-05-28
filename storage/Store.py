import cPickle as pickle
import time
import zipfile

DEFAULT_PATH = "store.zip"

class Store(object):

	class Error(Exception): pass
	class NotOpenError(Error): pass
	class OverwriteError(Error): pass

	PATH_TYPE_STR = 1
	PATH_TYPE_PICKLEABLE = 2

	def __init__(self, path=DEFAULT_PATH, pickled=True):
		self.path = path
		self.file = None
		self.pickled = pickled

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

	@classmethod
	def parse_path(cls, path_or_pickleable):
		if isinstance(path_or_pickleable, str):
			return path_or_pickleable, cls.PATH_TYPE_STR
		elif hasattr(path_or_pickleable, "derive_pickle_path"):
			return path_or_pickleable.derive_pickle_path(), cls.PATH_TYPE_PICKLEABLE
		else:
			raise TypeError("Store::parse_path: 1st argument `path_or_pickleable` is neither str nor Pickleable")

	def info(self, path_or_pickleable):
		if not self.file: raise self.NotOpenError("Store::info: can't query Store: Store not open() yet for business")
		path, path_type = self.parse_path(path_or_pickleable)
		try: return self.file.getinfo(path)
		except KeyError: return None

	@staticmethod
	def age_from_info(info):
		if not info: return None
		return time.mktime(time.strptime("%d-%d-%d/%d:%d:%d" % info.date_time, "%Y-%m-%d/%H:%M:%S"))

	@staticmethod
	def size_from_info(info):
		if not info: return None
		return info.file_size

	def add(self, path_or_pickleable, data=None, force=False):
		if not self.file: raise self.NotOpenError("Store::add: can't write to Store: Store not open() yet for business")

		path, path_type = self.parse_path(path_or_pickleable)

		if data is None:
			if self.PATH_TYPE_PICKLEABLE == path_type:
				data = path_or_pickleable
			# else: raise ValueError("Store::add: 2nd argument 'data' is None")

		if not force:
			try: extant_info = self.file.getinfo(path)
			except KeyError: pass
			else:
				zip_date_to_str = lambda d: "%d-%d-%d-%02d:%02d:%02d" % d
				raise self.OverwriteError("Store::add: path already exists at '%s' and force flag was not specified: ZipInfo{date: %s size: %d (%d) crc: %d}" % (path, zip_date_to_str(extant_info.date_time), extant_info.file_size, extant_info.compress_size, extant_info.CRC))

		if self.pickled:
			data = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)

		self.file.writestr(path, data)

	def get(self, path_or_pickleable):
		if not self.file: raise self.NotOpenError("Store::get: can't read from Store: Store not open() yet for business")

		path, path_type = self.parse_path(path_or_pickleable)

		try: data = self.file.read(path)
		except KeyError: return None

		if self.pickled:
			data = pickle.loads(data)

		return data

	def enum(self, ext=None, case_sensitive=False):
		if not self.file: raise self.NotOpenError("Store::enum: can't enumerate: Store not open() yet for business")
		if ext:
			ext_ = ext.lower() if ext else None
			has_ext_s = lambda p: p.endswith(ext) if ext else True
			has_ext_i = lambda p: p.lower().endswith(ext_) if ext_ else True
			has_ext = has_ext_s if case_sensitive else has_ext_i
			pp = (p for p in self.file.namelist() if has_ext(p))
		else:
			pp = (p for p in self.file.namelist())
		return iter(pp)
