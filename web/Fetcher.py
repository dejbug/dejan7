import cookielib
import os
import urllib2

from dejan7.web.Url import *

class Fetcher(object):

	@staticmethod
	def build_cookie_jar(jar_or_dict=None):
		jar = cookielib.CookieJar()
		if jar_or_dict is None: pass
		elif isinstance(jar_or_dict, cookielib.CookieJar):
			jar._cookies = jar_or_dict._cookies
		elif isinstance(jar_or_dict, dict):
			jar._cookies = jar_or_dict
		else: raise TypeError("build_cookie_jar: must be CookieJar or dict")
		return jar

	@classmethod
	def build_https_opener(cls, jar_or_dict=None):
		jar = cls.build_cookie_jar(jar_or_dict)
		return urllib2.build_opener(urllib2.HTTPSHandler, urllib2.HTTPCookieProcessor(jar), ), jar

	@staticmethod
	def is_fetched(url):
		url_filename = Url.get_unique_filename(url)
		return os.path.isfile(url_filename)

	@classmethod
	def fetch(cls, url, cookies={}):
		url = Url.normalize(url)
		opener, jar = cls.build_https_opener(cookies)
		page = opener.open(url)
		return page, jar._cookies
