
class RowInfo(object):

	def __init__(self, sci, row):
		self.row = row
		self.line = 0
		self.rows = 0
		self.first_row = 0
		self.last_row = 0

		lc = sci.GetLineCount()
		self.line = sci.DocLineFromVisible(self.row)

		if self.line >= lc:
			self.line = lc
			self.rows = 0
		else:
			self.rows = sci.WrapCount(self.line)

		self.first_row = sci.VisibleFromDocLine(self.line)
		self.last_row = self.first_row + self.rows - 1
