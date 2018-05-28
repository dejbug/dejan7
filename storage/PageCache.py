import os
import time

from dejan7.decorators.ToString import *
from dejan7.storage.Store import *
from dejan7.web.Page import *
from dejan7.web.Url import *

@ToString()
class PageCache(object):

	@ToString()
	class Source(object):
		def get_path(self, url): raise NotImplementedError
		def has_path(self, path): raise NotImplementedError
		def get_age_from_path(self, path): raise NotImplementedError
		def get_size_from_path(self, path): raise NotImplementedError

	class PathSource(Source):

		def __init__(self, path):
			assert isinstance(path, (str, unicode))
			self.path = path

		def get_path(self, url):
			page = Page(url)
			return os.path.join(self.path, page.filename)

		def has_path(self, path):
			return os.path.isfile(path)

		def get_size_from_path(self, path):
			if os.path.exists(path):
				return os.path.getsize(path)

		def get_age_from_path(self, path):
			if os.path.exists(path):
				return time.time() - os.path.getmtime(path)

		def load_from_path(self, path):
			if not os.path.isfile(path):
				return None
			with open(path, "rb") as f:
				return f.read()

	class StoreSource(Source):

		def __init__(self, store):
			assert isinstance(store, Store)
			self.store = store

		def get_path(self, url):
			page = Page(url)
			return page.filename

		def has_path(self, path):
			return self.store.info(path) is not None

		def get_size_from_path(self, path):
			info = self.store.info(path)
			if info:
				return Store.size_from_info(info)

		def get_age_from_path(self, path):
			info = self.store.info(path)
			if info:
				return time.time() - Store.age_from_info(info)

		def load_from_path(self, path):
			return self.store.get(path)

	def __init__(self, path_or_store=None):

		if path_or_store is None:
			self.source = self.PathSource(os.getcwd())
		elif isinstance(path_or_store, (str, unicode)):
			if os.path.exists(path_or_store) and not os.path.isdir(path_or_store):
				raise ValueError("PageCache::__init__: path '%s' is not a directory" % path_or_store)
			self.source = self.PathSource(os.path.abspath(path_or_store))
		elif isinstance(path_or_store, Store):
			self.source = self.StoreSource(path_or_store)
		else:
			raise TypeError("PageCache::__init__: 1st argument `path_or_store` is neither string nor Store")

	def get_path(self, url):
		return self.source.get_path(url)

	def get_age(self, url):
		path = self.source.get_path(url)
		return self.source.get_age_from_path(path)

	def get_size_from_path(self, path):
		return self.source.get_size_from_path(path)

	def is_expired(self, url, max_age=None):
		path = self.source.get_path(url)
		return self.is_expired_from_path(path, max_age)

	def is_expired_from_path(self, path, max_age=None):
		age = self.source.get_age_from_path(path)
		if age is None: return None
		return max_age is not None and age >= max_age

	def is_valid(self, url, max_age=None, empty_files_are_valid=False):
		path = self.source.get_path(url)
		if not self.source.has_path(path): return None
		if not empty_files_are_valid and 0 == self.get_size_from_path(path):
			return False
		return not self.is_expired_from_path(path, max_age)

	def exists(self, url):
		path = self.source.get_path(url)
		return self.source.has_path(path)

	def load(self, url):
		path = self.source.get_path(url)
		return self.source.load_from_path(path)

	def save(self, page):
		pass

	@classmethod
	def fetch(cls, url, cookies={}):
		obj = cls(url)
		return fetch_complete(obj)
