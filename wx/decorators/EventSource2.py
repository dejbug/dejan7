from collections import namedtuple

from wx.lib.pubsub import pub

def EventSource(name=""):

	def _(obj):

		Event_key = name + "Event"

		def PostEvent(self, *aa, **kk):
			kk["source"] = self
			Event = namedtuple(Event_key, " ".join(kk.keys()))
			pub.sendMessage(Event_key, e=Event(**kk))

		def SinkEvent(cls, callback, source=None, *aa, **kk):
			pub.subscribe(callback, Event_key, *aa, **kk)

		setattr(obj, "Post" + Event_key, PostEvent)
		setattr(obj, "Sink" + Event_key, classmethod(SinkEvent))

		return obj

	return _
