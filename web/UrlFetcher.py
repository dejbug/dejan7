import os
import pickle
import requests

class UrlFetcher(object):

	class Error(Exception): pass
	class OverwriteError(Error): pass

	@classmethod
	def fetch_page(cls, url, *aa, **kk):
		return requests.get(url, *aa, **kk)

	@classmethod
	def fetch_page_to_file(cls, file, url, *aa, **kk):
		pickle.dump(cls.fetch_page(url, *aa, **kk), file)

	@classmethod
	def fetch_page_to_path(cls, path, url, force=False, *aa, **kk):
		if not force and os.path.exists(path) and os.path.getsize(path):
			raise cls.OverwriteError("UrlFetcher.fetch_page_to_path: path already exists and force flag was not specified: '%s'" % path)
		with open(path, "wb") as file:
			cls.fetch_page_to_file(file, url, *aa, **kk)

	@classmethod
	def fetch_text(cls, url, *aa, **kk):
		return requests.get(url, *aa, **kk).text

	@classmethod
	def fetch_text_to_file(cls, file, url, *aa, **kk):
		file.write(cls.fetch_text(url, *aa, **kk))

	@classmethod
	def fetch_text_to_path(cls, path, url, force=False, *aa, **kk):
		if not force and os.path.exists(path) and os.path.getsize(path):
			raise cls.OverwriteError("UrlFetcher.fetch_text_to_path: path already exists and force flag was not specified: '%s'" % path)
		with open(path, "wb") as file:
			cls.fetch_text_to_file(file, url, *aa, **kk)
