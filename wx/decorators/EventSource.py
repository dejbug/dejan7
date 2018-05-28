import wx
import wx.lib.pubsub
import wx.lib.newevent


def EventSourcePS(decorated):
	"""This decorator uses pubsub. It is a simple wrapper around the
	already simple pubsub subscribe/sendMessage API. Instead of
	those two methods, we provide Subscribe() and PostEvent().
	"""

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
		"""Subscribe to a all or a specific event.

			Valid forms:
				Subscribe(event_cb) -- subscribe to all events
				Subscribe(event_id, event_cb) -- subscribe to one event
			Params:
				event_id -- An event's id (must be a string).
				event_cb -- The callback in case of event_id.

			NOTE: kwargs override args.
		"""

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
		"""Valid forms:
			PostEvent(event_id, **kwargs)
			PostEvent(**kwargs)
		"""
		if aa:
			event_id = root_event_id + "." + aa[0]
		else:
			event_id = root_event_id

		# import pdb; pdb.set_trace()
		wx.lib.pubsub.pub.sendMessage(event_id, **kk)

	setattr(decorated, "Subscribe", Subscribe)
	setattr(decorated, "PostEvent", PostEvent)

	return decorated


def EventSourceNE(decorated):
	"""This class uses newevent. It is provided for cases where
	EventSourcePS.PostEvent() doesn't work, e.g. from threading.Thread.run().

	Example:

	from dejan7.wx.decorators.EventSource import EventSourceNE

	@EventSourceNE
	class ThreadedDirlistLoader(object):
		def __init__(self):
			self.worker = None
			self.Event.SetToStringFormat("items")

		def Start(self, path):
			if self.worker:
				self.worker.join()

			self.worker = threading.Thread(target=self.Main, args=(path, ))
			self.worker.daemon = True
			self.worker.start()

		def Main(self, path):
			items = tuple(os.path.join(path, item) for item in os.listdir(path))
			self.PostEvent(items=items)

	class Frame(wx.Frame):

		def __init__(self):
			# ...
			self.Bind(ThreadedDirlistLoader.EVT, self.OnThreadedDirlistLoaderEvent)

		def OnThreadedDirlistLoaderEvent(self, e):
			print e

	"""

	def PostEvent(obj, *aa, **kk):
		if aa: aa[0].AddPendingEvent(obj.Event(wx.ID_ANY, **kk))
		else: wx.GetApp().GetTopWindow().AddPendingEvent(obj.Event(wx.ID_ANY, **kk))

	def SetToStringFormat(obj, keys):
		"""Call this e.g. from the decorated class's ctor to alter
		the way the Event object will print itself. If keys is None,
		the Event object's entire __dict__ will be printed. If keys
		is "" then all will be omitted. If it is a string like e.g.
		"self _cookie" then only self and __cookie will be included
		in the printout."""

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
