# import collections

def extend_missing_with_value(aa, bb, value=None):
	missing = len(aa) - len(bb)
	if missing > 0: bb.extend([value] * missing)
	return bb

def zip_extend(aa, values=[], *bbb):
	extend_missing_with_value(aa, values, None)
	return zip(aa, *[extend_missing_with_value(aa, bb, values[i]) for i, bb in enumerate(bbb)])

def apply_args_to_obj(obj, nn, *aa, **kk):
	extend_missing_with_value(nn, aa, None)
	# dd = collections.OrderedDict(zip(nn, aa))
	dd = dict(zip(nn, aa))
	dd.update(kk)
	# obj.__dict__ = dd
	obj.__dict__.update(dd)
