import base64
import os, os.path
import cPickle as pickle
import warnings
import zipfile


class FileCache(object):

	def __init__(self, path=u""):
		if not isinstance(path, unicode):
			raise TypeError("argument 'path' must be a unicode string")
		self.path = path.strip()
		if not self.path:
			self.path = u"cache.zip"
		self.path = os.path.abspath(self.path)
		if not os.path.exists(self.path):
			with zipfile.ZipFile(self.path, "w", zipfile.ZIP_DEFLATED):
				pass

	def has(self, path):
		with zipfile.ZipFile(self.path, "r", zipfile.ZIP_DEFLATED) as f:
			try: f.getinfo(path)
			except KeyError: return False
			else: return True

	def save(self, path, data, force=False):
		with zipfile.ZipFile(self.path, "a", zipfile.ZIP_DEFLATED) as f:
			if not force:
				try: f.getinfo(path)
				except KeyError: pass
				else: raise KeyError("path already exists")
			with warnings.catch_warnings():
				warnings.simplefilter("ignore")
				f.writestr(path, pickle.dumps(data, pickle.HIGHEST_PROTOCOL))

	def load(self, path):
		with zipfile.ZipFile(self.path, "r", zipfile.ZIP_DEFLATED) as f:
			try: return pickle.loads(f.read(path))
			except KeyError: pass


class FolderCache(object):
	
	MAX_PATH = 260

	def __init__(self, path=u"."):
		if not isinstance(path, unicode):
			raise TypeError("argument 'path' must be a unicode string")
		self.path = path.strip()
		if not self.path:
			self.path = u"."
		self.path = os.path.abspath(path)
		if not os.path.exists(self.path):
			os.mkdir(self.path)
		elif not os.path.isdir(self.path):
			raise ValueError("path exists but is not a folder: '%s'" % self.path)

	def encode_path(self, path):
		path = base64.b64encode(path, "+-")
		path = os.path.join(self.path, path)
		if len(path) > self.MAX_PATH:
			raise ValueError("path name is too long; consider using FileCache instead")
		return path

	def has(self, path):
		path = self.encode_path(path)
		return os.path.isfile(path)

	def save(self, path, data, force=False):
		path = self.encode_path(path)
		if not force and os.path.exists(path):
			raise KeyError("path already exists")
		with open(path, "wb") as f:
			f.write(data)

	def load(self, path):
		path = self.encode_path(path)
		if not os.path.isfile(path):
			raise KeyError("path does not exist")
		with open(path, "rb") as f:
			return f.read()
