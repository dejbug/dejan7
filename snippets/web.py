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
