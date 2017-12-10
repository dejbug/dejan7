
def SignatureDict(keys=None, cmp_filter=None):
	"""An object whose class was decorated with @SignatureDict(...) will
	print itself (almost) like a namedtuple.

	Keyword arguments:

	:param: `keys` (optional) A string of whitespace-separated identifiers.
	These are the names of the object attributes to be included in the
	output. If not specified (or None), all attributes will be included. If
	set to an empty string, all attributes will be excluded.

	:param: `cmp_filter` (optional) A callable that will receive the
	object's dictionary as its single argument and which must return a
	dictionary. This is used in determining whether an ellipsis ("...") will
	be printed to indicate that some attributes had been excluded from the
	output. The comparison is between the keyed dictionary and the filtered
	original.

	Examples:

	>>> from dejan7.decorators.SignatureDict import *
	>>>
	>>> @SignatureDict("hi_msg") # Include only the "hi_msg" attribute in
	...                          #   the signature.
	... class Greeter(object):
	...   def __init__(self):
	...     self.hi_msg = "Hi!"
	...     self.bye_msg = "Bye."
	...
	>>> print Greeter()
	Greeter{'hi_msg': 'Hi!', ...}

	To suppress the ellipsis in the output, in this case, we would pass a
	function something like this as `cmp_filter`:

	>>> f = lambda d: {k:v for k,v in d.items() if not k.endswith("_msg")}

	For example:

	>>> print SignatureDict("hi_msg", f)(Greeter)()
	Greeter{'hi_msg': 'Hi!'}

	Note: Observe that the filter is applied only to the original dict
	before comparison:

	>>> print SignatureDict(None, f)(Greeter)()
	Greeter{'hi_msg': 'Hi!', 'bye_msg': 'Bye.'}

	Note: It matters whether `keys` is pointed to an empty string or None.
	See here:

	>>> print SignatureDict()(Greeter)()
	Greeter{'hi_msg': 'Hi!', 'bye_msg': 'Bye.'}

	Compare this with:

	>>> print SignatureDict("")(Greeter)()
	Greeter{...}
	"""

	if keys and not isinstance(keys, str): raise TypeError("SignatureDict: 1st argument 'keys' must be a string (or None); did you mean to write @SignatureDict() ?")

	def _(cls):

		setattr(cls, "__repr__old", lambda self: super(cls, self).__repr__())

		setattr(cls, "__repr__", lambda self: self.__class__.__name__ + self.get_signature_dict_str())

		get_dict_str_with_ellipsis = lambda obj, keyed_dict: "{" + ", ".join(s for s in (str(keyed_dict)[1:-1], "...}") if s) if len(keyed_dict) < len(cmp_filter(obj.__dict__) if cmp_filter else obj.__dict__) else str(keyed_dict)

		setattr(cls, "get_signature_dict_str", lambda self: get_dict_str_with_ellipsis(self, self.get_signature_dict()))

		get_keyed_dict = lambda obj: {key : obj.__dict__[key] for key in keys.split()} if isinstance(keys, str) else obj.__dict__

		setattr(cls, "get_signature_dict", lambda self: get_keyed_dict(self))

		return cls

	return _

def _test():
	import doctest
	doctest.testmod()

if __name__ == "__main__":
	_test()
