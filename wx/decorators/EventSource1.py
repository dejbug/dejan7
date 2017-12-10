import wx, wx.lib.newevent


def EventSource(cls):
	assert issubclass(cls, wx.EvtHandler)

	Event, EVT = wx.lib.newevent.NewCommandEvent()
	setattr(cls, "Event", Event)
	setattr(cls, "EVT", EVT)

	def SendEvent(obj, action, *args, **kwargs):
		e = obj.Event(-1, source=obj, action=action, args=args, **kwargs)
		obj.ProcessEvent(e)

	def PostEvent(obj, action, *args, **kwargs):
		e = obj.Event(-1, source=obj, action=action, args=args, **kwargs)
		obj.AddPendingEvent(e)

	def PostEventTo(obj, target, action, *args, **kwargs):
		e = obj.Event(-1, source=obj, action=action, args=args, **kwargs)
		wx.PostEvent(target, e)

	def PostEventToTopWindow(obj, *aa, **kk):
		PostEventTo(obj, wx.GetApp().GetTopWindow(), *aa, **kk)

	setattr(cls, "SendEvent", SendEvent)
	setattr(cls, "PostEvent", PostEvent)
	setattr(cls, "PostEventTo", PostEventTo)
	setattr(cls, "PostEventToTopWindow", PostEventToTopWindow)

	return cls
