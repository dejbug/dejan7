import base64
import os.path
import pickle
import requests

def fetch(u, force=False):
	p = base64.b64encode(u, "+-")
	if force or not os.path.exists(p):
		r = requests.get(u)
		with open(p, "wb") as f:
			pickle.dump(r, f)
			return r
	else:
		with open(p, "rb") as f:
			return pickle.load(f)

if "__main__" == __name__:
	u = "https://www.ebay.de/sch/Mobel-Wohnen/11700/i.html?_from=R40&LH_BIN=1&_nkw=kaffeetisch&_dcat=38205&rt=nc&_mPrRngCbx=1&_udlo=4&_udhi=29"
	r = fetch(u)
	print r.status_code
	with open("sample.html", "wb") as f:
		f.write(r.text.encode("utf8"))
