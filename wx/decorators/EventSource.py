import wx
import wx.lib.pubsub
import wx.lib.newevent

## This class uses pubsub.
def EventSourcePS(decorated):

	# to_tuple_form = lambda s: [
	# 	n for n in map(lambda s: s.strip(), decorated.__name__.split(".")) if n
	# ]
	# root_event_id = to_tuple_form(decorated.__name__)
	
	root_event_id = decorated.__name__

	# def Subscribe(obj, event_id, callback):
	# 	wx.lib.pubsub.pub.subscribe(callback, event_id)

	## Subscribe(event_cb)
	## Subscribe(event_id, event_cb)
	def Subscribe(obj, *aa, **kk):
		## NOTE: kwargs override args.
		## TODO: 'event_id' should really be called sub_event_id.

		if "event_id" in kk:
			event_id = root_event_id + "." + kk["event_id"]
		else:
			if len(aa) >= 2:
				## The 'event_id' was specified as first argument in
				## 'Subscribe()'s two-argument form.
				event_id = root_event_id + "." + aa[0]
			else:
				# raise TypeError("missing 'event_id' argument")
				event_id = root_event_id

		if "event_cb" in kk:
			event_cb = kk["event_cb"]
		else:
			if len(aa) >= 2:
				event_cb = aa[1]
			elif len(aa) >= 1:
				event_cb = aa[0]
			else:
				raise TypeError("missing 'event_cb' argument")

		wx.lib.pubsub.pub.subscribe(event_cb, event_id)

	def PostEvent(obj, *aa, **kk):
		if aa:
			event_id = root_event_id + "." + aa[0]
		else:
			event_id = root_event_id
		
		# import pdb; pdb.set_trace()
		wx.lib.pubsub.pub.sendMessage(event_id, **kk)

	setattr(decorated, "Subscribe", Subscribe)
	setattr(decorated, "PostEvent", PostEvent)

	return decorated


## This class uses newevent
def EventSourceNE(decorated):

	def PostEvent(obj, *aa, **kk):
		if aa: aa[0].AddPendingEvent(obj.Event(wx.ID_ANY, **kk))
		else: wx.GetApp().GetTopWindow().AddPendingEvent(obj.Event(wx.ID_ANY, **kk))

	def SetToStringFormat(obj, keys):
		"""Call this e.g. from the decorated class's ctor to alter
		the way the Event object will print itself."""

		if isinstance(keys, str):
			keys = tuple(key for key in keys.split() if key)

		if None == keys:
			setattr(obj, "__str__",
				lambda self:
					"{0}.Event{1:s}".format(decorated.__name__, self.__dict__)
			)

		elif not keys:
			setattr(obj, "__str__",
				lambda self:
					"{0}.Event{{...}}".format(decorated.__name__)
			)

		else:
			setattr(obj, "__str__",
				lambda self:
					"{0}.Event{{... {1:s} ...}}".format(
						decorated.__name__,
						str({k:v for k,v in self.__dict__.items() if k in keys})[1:-1]
					)
			)
			
	Event, EVT = wx.lib.newevent.NewCommandEvent()

	setattr(decorated, "Event", Event)
	setattr(decorated, "EVT", EVT)
	setattr(decorated, "PostEvent", PostEvent)

	setattr(Event, "SetToStringFormat", classmethod(SetToStringFormat))

	return decorated
