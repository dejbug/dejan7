import re

import abstract
import storage

@abstract.NamedTuple("match_start match_end pretext_start pretext_end tagtext_start tagtext_end")
class TagOffset(object):
	re_tag = re.compile(r'(.*?)<(.+?)>', re.S)

	@classmethod
	def parse(cls, text):
		for x in cls.re_tag.finditer(r.text):
			yield cls(x.start(0), x.end(0), x.start(1), x.end(1), x.start(2), x.end(2))


if "__main__" == __name__:
	import web

	u = "https://www.ebay.de/sch/Mobel-Wohnen/11700/i.html?_from=R40&LH_BIN=1&_nkw=kaffeetisch&_dcat=38205&rt=nc&_mPrRngCbx=1&_udlo=4&_udhi=29"
	r = web.fetch(u)

	# with open("tag.offsets", "wb") as f:
	# 	storage.parse_to_pickle(TagOffset, f, r.text)

	with open("tag.offsets", "rb") as f:
		i = 0
		for tag in storage.parse_from_pickle(f):
			print tag
			print TagOffset(*tag.to_tuple())
			print TagOffset.from_obj(tag)
			print tag == TagOffset.from_obj(tag)
			print "-" * 78
			i += 1
			if i > 10: break
