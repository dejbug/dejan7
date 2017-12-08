import pickle

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

from dejan7.decorators.NamedTuple import *

@NamedTuple("name")
class StartTag(object): pass

@NamedTuple("name")
class EndTag(object): pass

@NamedTuple("key value value_raw")
class Attribute(object): pass

@NamedTuple("text text_raw")
class Data(object): pass

@NamedTuple("text text_raw")
class Comment(object): pass

@NamedTuple("text text_raw name")
class EntityRef(object): pass

@NamedTuple("text text_raw name")
class CharRef(object): pass

@NamedTuple("text")
class Decl(object): pass

class MemoryHTMLParser(HTMLParser):

	def __init__(self, mutable_seq=[]):
		HTMLParser.__init__(self)
		self.stack = mutable_seq

	def handle_starttag(self, tag, attrs):
		self.stack.append(StartTag(tag))
		for k, v in attrs:
			self.stack.append(Attribute(k, " ".join(v.split()) if v else "", v))

	def handle_endtag(self, tag):
		self.stack.append(EndTag(tag))

	def handle_data(self, data):
		self.stack.append(Data(" ".join(data.split()), data))

	def handle_comment(self, data):
		self.stack.append(Comment(" ".join(data.split()), data))

	def handle_entityref(self, name):
		try: c = unichr(name2codepoint[name])
		except KeyError: c = unicode("")
		self.stack.append(EntityRef(c, "&%s;" % name, name))

	def handle_charref(self, name):
		if name.startswith('x'):
			c = unichr(int(name[1:], 16))
			t = "&#x%s;" % name
		else:
			c = unichr(int(name))
			t = "&#%s;" % name
		self.stack.append(CharRef(c, t, name))

	def handle_decl(self, data):
		self.stack.append(Decl(data))
