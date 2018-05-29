import wx


class TextCtrlHelper(object):

	def __init__(self, parent):
		self.parent = parent

	def __getattr__(self, key):
		return getattr(self.parent, key)

	def GetRowIndexUnderCursor(self):
		window_mouse_pos = wx.GetMousePosition()
		client_mouse_pos = self.parent.ScreenToClient(window_mouse_pos)
		hit_ok, text_index_at_pos = self.parent.HitTestPos(client_mouse_pos)
		cell_ij_at_pos = self.parent.PositionToXY(text_index_at_pos)
		
		if hit_ok < 0: return None
		
		return cell_ij_at_pos[1]

	def GetFirstVisibleRowIndex(self):
		# return self.parent.PositionToXY(self.parent.HitTestPos((0,0))[1])[1]
		return self.parent.GetScrollPos(wx.VERTICAL)

	def GetLinesCount(self):
		return self.parent.GetScrollRange(wx.VERTICAL)
