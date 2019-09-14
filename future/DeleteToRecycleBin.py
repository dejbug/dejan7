__all__ = ["SHFileOperationW", "SHFileOperationA"]

import ctypes as C
import ctypes.wintypes as W
import os.path

# defined in: shellapi.h
FO_DELETE			= 0x3
FOF_SILENT			= 0x4
FOF_NOCONFIRMATION	= 0x10
FOF_ALLOWUNDO		= 0x40
FOF_FILESONLY		= 0x80
FOF_NOERRORUI		= 0x400

FILEOP_FLAGS = W.WORD

class SHFILEOPSTRUCTA(C.Structure):
	_fields_ = [
		("hwnd", W.HWND),
		("wFunc", C.c_uint),
		("pFrom", W.LPCSTR),
		("pTo", W.LPCSTR),
		("fFlags", FILEOP_FLAGS),
		("fAnyOperationsAborted", W.BOOL),
		("hNameMappings", C.c_void_p),
		("lpszProgressTitle", W.LPCSTR),
	]

class SHFILEOPSTRUCTW(C.Structure):
	_fields_ = [
		("hwnd", W.HWND),
		("wFunc", C.c_uint),
		("pFrom", W.LPCWSTR),
		("pTo", W.LPCWSTR),
		("fFlags", FILEOP_FLAGS),
		("fAnyOperationsAborted", W.BOOL),
		("hNameMappings", C.c_void_p),
		("lpszProgressTitle", W.LPCWSTR),
	]

LPSHFILEOPSTRUCTA = C.POINTER(SHFILEOPSTRUCTA)
LPSHFILEOPSTRUCTW = C.POINTER(SHFILEOPSTRUCTW)

NOERROR		= 0 # defined in: winerror.h
MAX_PATH	= 260 # defined in: minwindef.h

def win_hresult_errcheck(result, func, args):
	if NOERROR != result:
		raise C.WinError(result)
	return args
	
ProtoA = C.WINFUNCTYPE(C.c_int, LPSHFILEOPSTRUCTA)
ProtoW = C.WINFUNCTYPE(C.c_int, LPSHFILEOPSTRUCTW)

Paraf = (
	(1, "lpFileOp", None),
)

SHFileOperationA = ProtoA(("SHFileOperationA", C.windll.shell32), Paraf)
SHFileOperationA.errcheck = win_hresult_errcheck
SHFileOperationA._err_name = "SHFileOperationA"

SHFileOperationW = ProtoW(("SHFileOperationW", C.windll.shell32), Paraf)
SHFileOperationW.errcheck = win_hresult_errcheck
SHFileOperationW._err_name = "SHFileOperationW"


def DeleteToRecycleBin(path):
	assert isinstance(path, unicode), "path must be a unicode string"
	path = os.path.abspath(path)
	if os.path.isfile(path):
		path += u"\0\0"
		fop = SHFILEOPSTRUCTW(0, FO_DELETE, path, 0, FOF_SILENT | FOF_NOCONFIRMATION | FOF_NOERRORUI | FOF_ALLOWUNDO | FOF_FILESONLY, 0, 0, 0)
		SHFileOperationW(C.pointer(fop))

if "__main__" == __name__:
	test_path = u"~fj1092ylcxj0e923jalskdj0941.txt"
	if os.path.exists(test_path): exit(0)
	with open(test_path, "wb") as f:
		f.write("Hello recycle bin!")
	DeleteToRecycleBin(test_path)
