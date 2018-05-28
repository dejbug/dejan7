import cookielib

from dejan7.decorators.ToString import *

@ToString("_cookies")
class Jar(cookielib.CookieJar):

	@classmethod
	def from_obj(cls, o):
		if not o:
			return cls()
		elif isinstance(o, dict):
			return cls.from_dict(o)
		elif isinstance(o, cookielib.CookieJar):
			return cls.from_jar(o)
		else:
			raise TypeError("argument is neither `dict` nor `CookieJar`")

	@classmethod
	def from_dict(cls, d):
		jar = cls()
		jar._cookies = d
		return jar

	@classmethod
	def from_jar(cls, j):
		jar = cls()
		jar._cookies = j._cookies
		return jar

	def to_dict(self):
		return self._cookies

	def __getstate__(self):
		return self._cookies

	def __setstate__(self, state):
		self._cookies = state
