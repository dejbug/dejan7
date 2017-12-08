import web

if "__main__" == __name__:
	u = "https://www.ebay.de/sch/Mobel-Wohnen/11700/i.html?_from=R40&LH_BIN=1&_nkw=kaffeetisch&_dcat=38205&rt=nc&_mPrRngCbx=1&_udlo=4&_udhi=29"
	r = web.fetch(u)
	print r.status_code
