import httplib
import os
import StringIO
import time

from dejan7.storage.Store import *
from dejan7.web.Fetcher import *
from dejan7.web.Url import *

class Page(object):

	def __init__(self, url=None):
		assert url is None or isinstance(url, str)
		self.cookies = {}
		self.url = Url.normalize(url) if url else None
		self.rurl = None
		self.filename = Url.get_unique_filename(self.url) if url else None
		self.code = None
		self.headers = {}
		self.text = None

	def __repr__(self):
		return self.__class__.__name__ + str({k:(v if k != "text" else "'...'") for  k,v in self.__dict__.items()})

	@staticmethod
	def headers_from_info(info):
		assert isinstance(info, httplib.HTTPMessage)
		headers = dict(info)
		return headers

	@staticmethod
	def info_from_headers(headers):
		assert isinstance(headers, dict)
		text = "\r\n".join(("%s: %s" % it) for it in headers.items())
		file = StringIO.StringIO(text)
		return httplib.HTTPMessage(file)

	@classmethod
	def fetch_complete(cls, obj, cookies={}):
		page, obj.cookies = Fetcher.fetch(obj.url, cookies)
		obj.rurl = page.geturl()
		obj.code = page.getcode()
		obj.headers = cls.headers_from_info(page.info())
		obj.text = page.read()
		return obj

	@classmethod
	def fetch(cls, url, cookies={}):
		obj = cls(url)
		return fetch_complete(obj)

	@staticmethod
	def path_expired(path, max_age=None):
		assert isinstance(path, (str, unicode))
		if not os.path.exists(path):
			return None
		if max_age is None:
			return False
		return time.time() - os.path.getmtime(path) >= max_age

	@classmethod
	def fetch_from_path(cls, url, path=None, max_age=None):
		assert isinstance(url, (str, unicode))
		if not isinstance(path, (str, unicode)):
			obj = cls(url)
			path = obj.filename
		expired = cls.path_expired(path)
		if expired is None:
			## Path does not exist.
			return None, None
		if not os.path.isfile(path):
			## It's a directory: nothing to fetch.
			return None, expired
		with open(path, "rb") as f:
			return f.read(), expired
"""
	@classmethod
	def download(cls, url, cookies={}, path_or_store=None, max_age=None):

		obj = cls(url)

		## Which is the local path ?
		if path_or_store is None:
			path = obj.filename
		elif isinstance(path_or_store, (str, unicode)):
			path = path_or_store
		elif isinstance(path_or_store, Store):
			path = None
		else: raise TypeError("Page::download: 3rd argument `path_or_store` is neither string nor Store")

		## Is there something there already ?
		if path and os.path.exists(path):
			if not os.path.isfile(path):
				raise ValueError("Page::download: path '%s' already exists but is not a file" % path)
			if max_age is not None:
				age = time.time() - os.path.getmtime(path)
				if age < max_age:

		if store is None:
			return cls.fetch(url, cookies)

		page = cls.fetch(url)

		with Store() as store:
			store.add(page.filename, page)

		url_filename = Url.get_unique_filename(url)
		with Store() as store:
			print store.get(url_filename)
"""
