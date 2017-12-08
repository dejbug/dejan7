from dejan7.decorators.Pickleable import *

@Pickleable(".parser-res", "job")
class ParserResult(object):

	def __init__(self, job, data):
		self.job = job
		self.data = data
