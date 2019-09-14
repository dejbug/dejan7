import cookielib, urllib, urllib2, urlparse
import io, gzip
import base64


class Response(object):

	def __init__(self, req=None, cookies={}, headers={}, rurl="", text=""):

		assert isinstance(req, Request)
		assert isinstance(cookies, dict)
		assert isinstance(headers, dict)
		assert isinstance(rurl, str)
		assert isinstance(text, str)

		self.req = req
		self.cookies = cookies
		self.headers = headers
		self.rurl = rurl
		self.text = text

	def __str__(self):
		return "Response{{req={0[req]:s}, cookies={0[cookies]}, headers={0[headers]}, rurl={0[rurl]}, text=...}}".format(self.__dict__)


class Request(object):

	STANDARD_HEADERS = {
		"User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"Accept-Encoding": "gzip, deflate",
		"Connection": "keep-alive",
	}

	def __init__(self, url, data={}, cookies={}, headers={}, timeout=None, referer=None):

		assert isinstance(url, str)
		assert isinstance(data, dict)
		assert isinstance(cookies, dict)
		assert isinstance(headers, dict)
		assert None is timeout or isinstance(timeout, float)
		assert None is referer or isinstance(referer, str)
		
		self.url = url
		self.data = data
		self.cookies = cookies
		self.headers = headers if headers else self.STANDARD_HEADERS
		self.timeout = timeout
		self.referer = referer

	def __str__(self):
		return "Request{{url={0[url]}, data={0[data]}, cookies={0[cookies]}, headers={0[headers]}, timeout={0[timeout]}, referer={0[referer]}}}".format(self.__dict__)


def fetch(req):
	
	data = urllib.urlencode(data) if req.data else None

	r = urllib2.Request(req.url, data)

	if req.headers:
		for k, v in req.headers.items():
			r.add_header(k, v)

	if req.referer:
		r.add_header("Referer", req.referer)

	jar = cookielib.CookieJar()
	jar._cookies = req.cookies

	opener = urllib2.build_opener(urllib2.HTTPSHandler(), urllib2.HTTPCookieProcessor(jar))
	p = opener.open(r, timeout=req.timeout)

	text = p.read()
	rurl = p.geturl()
	headers = p.info()

	if "Content-Encoding" in headers:
		if "gzip" == headers["Content-Encoding"]:
			text = un_gzip_text(text)

	return Response(req, jar._cookies, dict(headers), rurl, text)


def un_gzip_text(t):
	assert isinstance(t, str)
	f = io.BytesIO(t)
	z = gzip.GzipFile(fileobj=f)
	return z.read()


def hash(req_or_res):
	assert isinstance(req_or_res, (str, Request, Response))
	if isinstance(req_or_res, str):
		url = req_or_res
	elif isinstance(req_or_res, Request):
		url = req_or_res.url
	elif isinstance(req_or_res, Response):
		url = req_or_res.req.url
	assert isinstance(url, str)
	url = url.strip().lower()
	path = base64.b64encode(url, "+-")
	return path
