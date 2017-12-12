import wx.stc

from dejan7.wx.stc.RowInfo import *

def GetLastWrappedRowsY(sci, all_lines=True):
	rh = sci.TextHeight(0)
	rc = sci.LinesOnScreen()
	fvr = sci.GetFirstVisibleLine()

	yy = []
	ly = 0

	for i in xrange(fvr, fvr + rc):
		ri = RowInfo(sci, i);

		if all_lines or ri.rows > 1:
			y = rh * (ri.rows - (fvr - ri.first_row))
			if y != ly: yy.append(y)
			ly = y

	return yy

def GetColumnCounts(sci):
	s = sci.GetClientSize()

	row_height = sci.TextHeight(0)
	row_count = sci.LinesOnScreen()

	cc = []

	for row in xrange(row_count):
		# ri = RowInfo(sci, row)

		y = row * row_height

		start_pos = sci.CharPositionFromPoint(0, y)
		start_col = sci.GetColumn(start_pos)

		end_pos = sci.CharPositionFromPoint(s.width, y)
		end_col = sci.GetColumn(end_pos)

		cc.append(end_col - start_col)

	return cc

def GetRowWidths(sci, air=3, margins=[]):
	mw = sum(map(sci.GetMarginWidth, margins))
	cw = sci.TextWidth(wx.stc.STC_STYLE_DEFAULT, "X")
	cc = GetColumnCounts(sci)

	return tuple((mw + c * cw + air if c > 0 else -1) for c in cc)
