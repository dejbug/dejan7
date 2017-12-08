import requests

from dejan7.decorators.Pickleable import *
# from dejan7.snippets import web

from MemoryHTMLParser import *
from ParserResult import *

@Pickleable(".parser-job", "url")
class ParserJob(object):

	def __init__(self, url):
		self.url = url

	def derive_result_pickle_path(self):
		return ParserResult(self, None).derive_pickle_path()

	def parse(self, url=None):
		if not url: url = self.url
		# r = web.fetch(url)
		r = requests.get(url)
		parser = MemoryHTMLParser()
		parser.feed(r.text)
		return ParserResult(self, parser.stack)
