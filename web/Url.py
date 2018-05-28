import base64
import re
import urllib
import urlparse

from dejan7.abstract.ordict import *

class Url(object):

	DEFAULT_SCHEME = "https"
	SPLIT_KEYS = ("scheme", "netloc", "path", "query", "fragment")
	SPLIT_EX_KEYS = ("scheme", "hostname", "port", "username", "password", "path", "query", "fragment")

	@classmethod
	def split(cls, url):
		"""
		>>> Url.split("https://youtube.com/watch?v=gr0XWmEbiMQ")
		ordict[scheme='https', netloc='youtube.com', path='/watch', query='v=gr0XWmEbiMQ', fragment='']
		"""
		up = urlparse.urlsplit(url, scheme=cls.DEFAULT_SCHEME)
		return ordict((k, v) for k,v in zip(cls.SPLIT_KEYS, up))

	@classmethod
	def split_ex(cls, url):
		"""
		>>> Url.split_ex("https://admin@youtube.com:89/watch?v=gr0XWmEbiMQ")
		ordict[scheme='https', hostname='youtube.com', port=89, username='admin', password=None, path='/watch', query='v=gr0XWmEbiMQ', fragment='']
		"""
		up = urlparse.urlparse(url, scheme=cls.DEFAULT_SCHEME)
		return ordict((k, getattr(up, k, '')) for k in cls.SPLIT_EX_KEYS)

	@staticmethod
	def make_netloc(hostname, port=80, username=None, password=None):
		"""
		>>> Url.make_netloc("youtube.com", "80", None, None)
		'youtube.com:80'
		>>> Url.make_netloc("youtube.com", "80", "", None)
		'@youtube.com:80'
		>>> Url.make_netloc("youtube.com", "80", "", "")
		':@youtube.com:80'
		"""
		s = ""
		if username is not None:
			s += username
			if password is not None:
				s += ":" + password
			s += "@"
		# hostname = hostname.lower()
		s += hostname
		if port is not None:
			s += ":" + str(port)
		return s

	@classmethod
	def normalize(cls, url):
		"""
		>>> Url.normalize("HTTPs://Admin:1234@YouTube.com//watch?v=gr0XWmEbiMQ&start=10m5s&end=")
		'https://Admin:1234@youtube.com/watch?start=10m5s&v=gr0XWmEbiMQ'
		"""
		us = cls.split_ex(url)

		# us.scheme = us.scheme.lower()
		qs = urlparse.parse_qs(us.query, keep_blank_values=False)
		us.query = urllib.urlencode(qs, doseq=True)
		us.path = re.sub("//+", "/", us.path)

		netloc = cls.make_netloc(us.hostname, us.port, us.username, us.password)
		return urlparse.urlunsplit((us.scheme, netloc, us.path, us.query, us.fragment))

	@staticmethod
	def get_query_dict(url):
		"""
		>>> Url.get_query_dict("https://www.youtube.com/watch?v=gr0XWmEbiMQ&t=10m5s")
		{'t': '10m5s', 'v': 'gr0XWmEbiMQ'}
		"""
		up = urlparse.urlsplit(url)
		qs = urlparse.parse_qs(up.query, keep_blank_values=True)
		pop_func = lambda seq: seq[0] if len(seq) == 1 else seq
		return {k:pop_func(v) for k,v in qs.items()}

	@classmethod
	def set_query_dict(cls, url, qs):
		"""
		>>> Url.set_query_dict("https://www.youtube.com/watch", {'t': '10m5s', 'v': 'gr0XWmEbiMQ'})
		'https://www.youtube.com/watch?t=10m5s&v=gr0XWmEbiMQ'
		"""
		assert isinstance(qs, dict)
		us = cls.split(url)
		us.query = urllib.urlencode(qs, doseq=True)
		return urlparse.urlunsplit(us.values())

	@classmethod
	def update_query_dict(cls, url, qs):
		"""
		>>> Url.update_query_dict("https://www.youtube.com/watch?v=gr0XWmEbiMQ", {"t":"10m5s"})
		'https://www.youtube.com/watch?t=10m5s&v=gr0XWmEbiMQ'
		"""
		assert isinstance(qs, dict)
		_qs = cls.get_query_dict(url)
		_qs.update(qs)
		return cls.set_query_dict(url, _qs)

	@classmethod
	def get_unique_filename(cls, url):
		"""
		>>> Url.get_unique_filename("https://www.youtube.com")
		'aHR0cHM6Ly93d3cueW91dHViZS5jb20='
		"""
		url = cls.normalize(url)
		return base64.b64encode(url, "+-")

def _test():
	import doctest
	doctest.testmod()

if "__main__" == __name__:
	_test()
