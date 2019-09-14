import ctypes
import re
import sys


class Error(Exception): pass
class TestError(Error): pass
class ArgumentError(Error): pass


class COORD(ctypes.Structure):
	_fields_ = [("X", ctypes.c_short),
				("Y", ctypes.c_short)]


class SMALL_RECT(ctypes.Structure):
	_fields_ = [("Left", ctypes.c_short),
				("Top", ctypes.c_short),
				("Right", ctypes.c_short),
				("Bottom", ctypes.c_short)]


class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
	_fields_ = [("dwSize", COORD),
				("dwCursorPosition", COORD),
				("wAttributes", ctypes.c_ushort),
				("srWindow", SMALL_RECT),
				("dwMaximumWindowSize", COORD)]


STD_OUTPUT_HANDLE = 0xfffffff5

FOREGROUND_BLUE			= 0x01
FOREGROUND_GREEN		= 0x02
FOREGROUND_RED			= 0x04
FOREGROUND_INTENSITY	= 0x08
BACKGROUND_BLUE			= 0x10
BACKGROUND_GREEN		= 0x20
BACKGROUND_RED			= 0x40
BACKGROUND_INTENSITY	= 0x80

FG_RED		= FOREGROUND_RED
FG_GREEN	= FOREGROUND_GREEN
FG_BLUE		= FOREGROUND_BLUE
FG_BRIGHT	= FOREGROUND_INTENSITY
BG_RED		= BACKGROUND_RED
BG_GREEN	= BACKGROUND_GREEN
BG_BLUE		= BACKGROUND_BLUE
BG_BRIGHT	= BACKGROUND_INTENSITY

DARK_RED	= FOREGROUND_RED
DARK_GREEN	= FOREGROUND_GREEN
DARK_BLUE	= FOREGROUND_BLUE
DARK_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN
DARK_WHITE	= FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE

BLACK, NAVY, GREEN, TEAL, BROWN, VIOLET, GOLD, LIGHT_GREY, DARK_GREY, BLUE, GREEN, TURQUOISE, RED, PINK, YELLOW, WHITE = range(16)


colors = {

	"black":		BLACK,		# 0
	"blue":			FG_BLUE,	# 1
	"green":		FG_GREEN,	# 2
	"aqua":			FG_GREEN | FG_BLUE,	# 3
	"red":			FG_RED,				# 4
	"purple":		FG_RED | FG_BLUE,	# 5
	"yellow":		FG_RED | FG_GREEN,	# 6
	"light grey":	FG_RED | FG_GREEN | FG_BLUE,	# 7
	"grey":			FG_BRIGHT | BLACK,	# 8
	"light blue":	FG_BRIGHT | FG_BLUE,	# 9
	"light green":	FG_BRIGHT | FG_GREEN,	# 10
	"light aqua":	FG_BRIGHT | FG_GREEN | FG_BLUE,	# 11
	"light red":	FG_BRIGHT | FG_RED,				# 12
	"light purple":	FG_BRIGHT | FG_RED | FG_BLUE,	# 13
	"light yellow":	FG_BRIGHT | FG_RED | FG_GREEN,	# 14
	"white":		FG_BRIGHT | FG_RED | FG_GREEN | FG_BLUE,	# 15
	
	## alternative names:
	"orange":		FG_RED | FG_GREEN,	# 6
	"light gray":	FG_RED | FG_GREEN | FG_BLUE,	# 7
	"gray":			FG_BRIGHT | BLACK,	# 8
	"pink":			FG_BRIGHT | FG_RED | FG_BLUE,	# 13
}


def writeln(text, color=None, safe=True):
	"""Write a (colored) line."""
	
	if safe and re.search("[\r\n]", text):
		raise ArgumentError, "text must not contain line breaks!"
	
	if None == color:
		sys.stdout.write(text)
		sys.stdout.write("\r\n")
	else:
		if isinstance(color, (int, long, str, unicode)):
			color = Color(color)
		
		if not isinstance(color, Color):
			raise ArgumentError, "invalid color argument"
		
		color.apply()
		sys.stdout.write(text)
		color.reset()
		sys.stdout.write("\r\n")
		

def write(text, color=None, safe=True):
	"""Write (colored) text."""
	
	if safe and re.search("[\r\n]", text):
		raise ArgumentError, "text must not contain line breaks!"
		
	if None == color:
		sys.stdout.write(text)
	else:
		if isinstance(color, (int, long, str, unicode)):
			color = Color(color)
		
		if not isinstance(color, Color):
			raise ArgumentError, "invalid color argument"
		
		color.apply()
		sys.stdout.write(text)
		color.reset()
		
		
def writep(text, color=None):
	"""Write a (colored) paragraph."""
	
	if None == color:
		sys.stdout.write(text)
	else:
		if isinstance(color, (int, long, str, unicode)):
			color = Color(color)
		
		if not isinstance(color, Color):
			raise ArgumentError, "invalid color argument"
		
		lines = re.split(r'(\r?\n)', text)
		lines.append("")
		
		assert len(lines) % 2 == 0
		
		for i in xrange(0, len(lines), 2):
			color.apply()
			sys.stdout.write(lines[i])
			color.reset()
			
			sys.stdout.write(lines[i+1])
		

fg_to_fb = lambda fg: fg & 0x0f
bg_to_fb = lambda bg: bg & 0xf0
fgbg_to_fb = lambda fg, bg: (bg << 4) & 0xf0 | fg & 0x0f
fb_to_fgbg = lambda fb: (fb & 0x0f, (fb >> 4) & 0x0f)


def query():
	"""Return the consoles current colors.

	The color will be in 'packed' integer form. Call fb_to_fgbg() to unpack it.
	"""
	handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
	csbi = CONSOLE_SCREEN_BUFFER_INFO()
	ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle, ctypes.pointer(csbi))
	return csbi.wAttributes
	

class Color(object):

	def __init__(self, *aa, **kk):
		"""Usage:

		Color()
		Color("black on white")
		Color("black")
		Color("on white")
		Color(fg="black")
		Color(fg="black", bg="white")
		"""

		## Remember the current console color state.
		## (Read "fb" as "foreground + background".)
		
		self._fb_original = query()

		## Now parse the arguments.

		self.extend_kk_with_aa(kk, aa)

		## If we're here, we know that kk has the
		## fg and bg items set to something.

		self.fg = self.get_fg_from_selector(kk["fg"])
		self.bg = self.get_bg_from_selector(kk["bg"])

	def reset(self):
		"""Reset the console's colors to what they
		were before we made changes.
		"""
		handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
		ctypes.windll.kernel32.SetConsoleTextAttribute(handle, self._fb_original)
		
	def apply(self):
		"""Save our colors to the console, so that
		it reflects our state.
		"""
		handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)	
		ctypes.windll.kernel32.SetConsoleTextAttribute(handle, self.pack())

	def update(self):
		"""Load our current colors from the current
		console colors. So our state reflects the
		console's.
		"""
		self.fb, self.fg = fb_to_fgbg(query())

	def pack(self):
		"""Pack our colors. If any of our colors is
		None, substitute the console's original for it.
		"""
		ofg, obg = fb_to_fgbg(self._fb_original)
		fg = ofg if self.fg is None else self.fg
		bg = obg if self.bg is None else self.bg
		return fgbg_to_fb(fg, bg)

	@classmethod
	def translate_on_string(cls, text):
		"""Just in case this string is of the form
		"... on ...", this will split it and return
		("...", "..."). Either one of the components
		may be missing, in that case it is replaced
		by None; e.g. "on abc de" -> (None, "abc de").
		"""
		norm = lambda t: t.strip().lower()

		try:
			fgbg = text.split("on")

			if len(fgbg) == 1:
				return norm(fgbg[0]), None

			elif len(fgbg) == 2:
				return norm(fgbg[0]), norm(fgbg[1])

		except: pass

		## This should never happen if |text| was
		## a string.
		return None, None
		
	@classmethod
	def extend_kk_with_aa(cls, kk, aa):

		"""Merge the relevant aa-list entries into
		the kk-dict. This is called from the ctor.
		
		('kk' and 'aa' are our aliases for kwargs &c.)

		When this finishes, kk will have its "fg"
		and "bg" keys set to something (anything
		really; actual color selectors, we hope).
		"""

		## If kk already has "fg" and "bg" keys
		## we need to skip the aa handling entire;
		## because if the user has gone through
		## the trouble of typing the keywords, they
		## must be really special to him or her.

		if "fg" in kk and "bg" in kk:
			return

		## We know now that one of the two required
		## keys is missing.

		if len(aa) == 0:

			## No additional info was provided by by
			## the user.

			aa = (None, None)

		elif len(aa) == 1:

			## We've got one argument.

			## If it's another Color object, we can
			## assume that it has finished doing
			## what we're doing now, so we simply
			## copy over and we're done.

			if isinstance(aa[0], Color):
				kk[fg] = aa[0].fg
				kk[bg] = aa[0].bg
				return

			## From this point onward we won't accept
			## anything but a string. So just in
			## case it is something else after all
			## we will try to force it into shape.

			if not isinstance(aa[0], (str, unicode)):
				aa[0] = str(aa[0])
		
			## We know it's a string now. It could
			## be the fg or an fg-on-bg selector.
			## So we drop our aa and replace it with
			## a better one.
			aa = cls.translate_on_string(aa[0])
		
		## At this point we know that we have two
		## arguments in aa (at least two, at last).

		if len(aa) >= 2:

			## We got two arguments, so they will
			## be treated as fg and bg. We'll only
			## apply to kk what is missing. Again,
			## if the user went through the trouble
			## of typing out the fg and/or bg
			## keywords, despite the easier "on"
			## syntax, we must respect that.

			if "fg" not in kk:
				kk["fg"] = aa[0]

			if "bg" not in kk:
				kk["bg"] = aa[1]

		# import pprint
		# pprint.pprint(kk)

		## This can never happen.
		# if "fg" not in kk or "bg" not in kk:
		# 	raise ArgumentError("missing arguments")

	@classmethod
	def get_colors_from_selector(cls, sel):
		"""Return a tuple (fg, bg) of integers,
		specifying valid color identifiers. If the
		selector specifies only a single color, but
		it is not clear whether that color is fg
		or bg, both will be set. If it is clear, then
		the other color will be None.

		The color identifiers returned are "valid"
		in the sense that they will be able to be
		used with the pack() method.
		"""

		if isinstance(sel, Color):
			## It's another Color instance. We can
			## assume that it completed running its
			## ctor.
			return (sel.fg, sel.bg)

		if isinstance(sel, (int, long)):
			## It's a number. We clamp it.
			return fb_to_fgbg(sel)

		## From this point on we want to assume
		## that a string was passed.

		if not isinstance(sel, (str, unicode)):
			## We force it to string.
			sel = str(sel)

		## We're done.

		c = colors[sel] if sel in colors else None
		
		return (c, c)

	@classmethod
	def get_fg_from_selector(cls, sel):
		return cls.get_colors_from_selector(sel)[0]

	@classmethod
	def get_bg_from_selector(cls, sel):
		return cls.get_colors_from_selector(sel)[1]
