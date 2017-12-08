from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

class OutputHTMLParser(HTMLParser):

	def __init__(self, file):
		HTMLParser.__init__(self)
		self.file = file

	def handle_starttag(self, tag, attrs):
		# aa = " ".join("%s='%s'" % (k, unicode(v)) for k,v in attrs)
		# self.file.write("+ %s (%s)\n" % (tag, aa))
		self.file.write("+ %s (" % tag)
		for k, v in attrs:
			self.file.write("\n\t%s: '%s'" % (k, v))
		self.file.write("%s)\n" % ("\n" if len(attrs) else ""))

	def handle_endtag(self, tag):
		self.file.write("- %s\n" % tag)

	def handle_data(self, data):
		data = " ".join(data.split())
		if data: self.file.write("= '%s'\n" % data)

	def handle_comment(self, data):
		data = " ".join(data.split())
		if data: self.file.write("* '%s'\n" % data)

	def handle_entityref(self, name):
		c = unichr(name2codepoint[name])
		self.file.write("= '%s' (%s) {entityref}\n" % (c, name))

	def handle_charref(self, name):
		if name.startswith('x'):
			c = unichr(int(name[1:], 16))
		else:
			c = unichr(int(name))
		self.file.write("= '%s' (%s) {charref}\n" % (c, name))

	def handle_decl(self, data):
		self.file.write("! '%s'\n" % data)
