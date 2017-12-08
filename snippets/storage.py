import os
import pickle

class Error(Exception): pass
class OverWriteError(Error): pass

def parse_to_pickle(cls_or_obj, file, text):
	return pickle.dump(tuple(cls_or_obj.parse(text)), file)

def parse_from_pickle(file):
	return pickle.load(file)

def save_to_pickle(thing, obj=None, force=False):
	if hasattr(thing, "write"):
		save_to_pickle_file(thing, obj)
	elif isinstance(thing, (str, unicode)):
		save_to_pickle_path(thing, obj, force=force)
	elif hasattr(thing, "derive_pickle_path"):
		save_to_pickle_path(thing.derive_pickle_path(), thing, force=force)
	else:
		raise ValueError("save_to_pickle: 1st argument 'thing' is neither a valid file object nor a path string nor a Query object")

def save_to_pickle_file(f, obj):
	assert hasattr(f, "write")
	pickle.dump(obj, f)

def save_to_pickle_path(p, obj, force=False):
	assert isinstance(p, (str, unicode))
	if not force and os.path.exists(p):
		raise OverWriteError("save_to_pickle_path: path already exists for %s object and force flag was not specified: '%s'" % (obj.__class__.__name__, p))
	with open(p, "wb") as f:
		save_to_pickle_file(f, obj)
