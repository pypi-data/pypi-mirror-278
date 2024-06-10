"""
============================================================================
==THIS IS PROBABLY NOT THE FEATURE-COMPLETE RDS PARSER YOU ARE LOOKING FOR==
============================================================================
This code was written for and exclusively tested on RDS files representing
SeuratObject data. Missing SEXPTYPE parsing is indicated by the 
SEXPTYPE_Parser subclasses whose parse() methods raise a 
NotImplementedError. In addition, this code likely includes 
oversimplifications or unintentional hacks that may not work with any or 
all other valid serialized data. It is not recommended that this code be 
applied as-is to serialized data other than SeuratObject data.
============================================================================

Python representation of a SeuratObject as loaded directly from an RDS file

Almost all of this is based on the writing here: 
https://blog.djnavarro.net/posts/2021-11-15_serialisation-with-rds/#serialising-to-plain-text-rds

and the R internals manual here:
https://cran.r-project.org/doc/manuals/r-release/R-ints.pdf
"""


from abc import abstractmethod
import gzip
from os import altsep, curdir
from typing import cast, Dict, List, Optional, Tuple, TypedDict, Union
from typing_extensions import Self
import struct
import sys


class SeuratObjectRDS:
	"""
	Python representation of Seurat data directly from an RDS file. Purpose is to have
	access to an RDS-encoded `SeuratObject` data structure without having Seurat or R
	installed. 

	Header info
	- 2 bytes for format
	- 4 bytes for serialization version
	- 8 bytes for R version
	- 4 bytes for encoding length
	- n bytes for whatever encoding length is
	- So minimum header is 18 bytes + whatever the encoding is
	"""
	filepath: str
	debug_bytes: int
	xdr_hex: List[str]
	header_length: int
	encoding_length: int
	encoding: str
	r_writing_version: int
	r_minimum_version: int
	data: List

	char_cache: Dict[int, str] = {}

	hit_commands: bool = False

	def __init__(
		self: Self,
		filepath: str,
		debug_bytes: int = 0
	) -> None:
		"""
		Driver for loading and parsing RDS data for a SeuratObject.

		Parameters
		----------
		filepath : str
			Path to the RDS file
		debug_bytes : int
			If greater than 0, only load the number of bytes specified, otherwise disregard
		"""
		self.filepath = filepath
		self.debug_bytes = debug_bytes


	def __str__(self: Self) -> str:
		"""
		Print some metadata
		"""
		ret_str = (
			f"SeuratObjectRDS\n"
			f"---------------\n"
			f"filepath = {self.filepath}\n"
			f"encoding = {self.encoding}\n"
			f"r_writing_version = {self._decode_r_version(self.r_writing_version)}\n"
			f"r_minimum_version = {self._decode_r_version(self.r_minimum_version)}\n"
			f"size (bytes) = {len(self.xdr_hex)}"
		)

		return ret_str


	def _get_hex_bytes(
		self: Self,
		start: int,
		n_bytes: int
	) -> List[str]:
		"""
		Get a segment of the hex-encoded data inclusive of the end

		Parameters
		----------
		start : int
			0-indexed starting position in the hex data to slice
		n_bytes : int
			Number of bytes to retrieve, including start

		Returns
		-------
		List[str]
			The slice of the hex string requested
		"""
		return self.xdr_hex[start:start+n_bytes]


	def _get_ascii_from_hex_bytes(
		self: Self,
		hex_bytes: List[str]
	) -> str:
		"""
		Given a list of hex-encoded bytes, return an ASCII string.

		Parameters
		----------
		hex_bytes : List[str]
			List of two-character hex strings, each representing a byte.

		Returns
		-------
		str
			The ASCII string decoded from the hex bytes.
		"""
		return bytearray.fromhex(''.join(hex_bytes)).decode()


	class RDSFormatError(Exception):
		"""
		Error to raise if the format byte is not "X" (0x58)
		"""
		def __init__(
			self: Self, 
			format_byte: str
		) -> None:
			"""
			Construct message to alert that the format byte indicates this file
			is not the modern binary format.

			Parameters
			----------
			format_byte : str
				The two-character hex string encoding the format. This code requires
				this byte to be 0x58, i.e., "X".
			"""
			super().__init__(f"Got format byte 0x{format_byte}, expected 0x58 ('X')")


	def _check_format(
		self: Self
	) -> None:
		"""
		Checks if expected format byte 0x58 is seen at the beginning of the file.
		"""
		format_byte = self._get_hex_bytes(0, 1)[0]
		
		if format_byte != "58":
			raise self.RDSFormatError(format_byte)


	def load_tokens(
		self: Self
	) -> None:
		"""
		Parses an RDS into string tokens as described in the blog post linked above.

		Returns
		-------
		List[str]
			A list of tokens representing the data and structure of the RDS file as described
			in the R internals manual linked above.
		"""
		with gzip.open(self.filepath, 'rb') as f:
			if self.debug_bytes > 0:
				rds_bytes = f.read(self.debug_bytes)
			else:
				rds_bytes = f.read()

		xdr_hex_pairs = [
			rds_bytes[i:i+1].hex()
			for i in range(len(rds_bytes))
		]

		self.xdr_hex = xdr_hex_pairs

		self._check_format()


	def _get_int_from_hex(
		self: Self,
		hex_bytes: List[str]
	) -> int:
		"""
		Given a string of hex bytes, interpret it as an integer.

		Parameters
		----------
		hex_bytes : List[str]
			The list of hex character pairs forming bytes of an int.

		Returns
		-------
		int
			A base-10 integer encoded by `hex_bytes`.
		"""
		return int(''.join(hex_bytes), 16)


	def _get_chars_from_hex(
		self: Self,
		hex_bytes: List[str]
	) -> str:
		"""
		Given a string of hex bytes, interpret it as a character string.

		Parameters
		----------
		hex_bytes : List[str]
			The list of hex character pairs forming bytes of a string.

		Returns
		-------
		str
			The string encoded by `hex_bytes`.
		"""
		ascii_str = ""

		for byte in hex_bytes:
			#if 0x20 < int(byte, 16) < 0x7F or int(byte, 16) == 0:
			if int(byte, 16) < 0x7F:
				ascii_str = ascii_str + bytearray([int(byte, 16)]).decode()
			else:
				raise ValueError(f"Got byte {byte}, cannot be interpreted as a printable ASCII character")

		return ascii_str


	def _get_encoding(
		self: Self
	) -> str:
		"""
		Uses `self.encoding_length` to extract the name of the string encoding
		used in this RDS file.
		"""
		self.encoding_length = self._get_int_from_hex(self._get_hex_bytes(14, 4))
		encoding_bytes = self._get_hex_bytes(18, self.encoding_length)
		return self._get_ascii_from_hex_bytes(encoding_bytes)


	def _get_r_versions(
		self: Self
	) -> None:
		"""
		Retrieves the R written version and the minimum required version from the header
		and populates the appropriate fields.
		"""
		self.r_writing_version = self._get_int_from_hex(self._get_hex_bytes(6, 4))
		self.r_minimum_version = self._get_int_from_hex(self._get_hex_bytes(10, 4))


	def _decode_r_version(
		self: Self,
		version: int
	) -> str:
		"""
		Returns a string version of an integer representing an R version according to
		(major * 65536) + (minor * 256) + patch

		Source: https://blog.djnavarro.net/posts/2021-11-15_serialisation-with-rds/#how-does-rds-serialisation-work
		"""
		major = (version >> 16) & 0x000f
		minor = (version >> 8) & 0x000f
		patch = version & 0x000f

		return f"{major}.{minor}.{patch}"


	def parse_header(
		self: Self
	) -> None:
		"""
		Parses the header and checks if the RDS file is compatible with this code. 
		"""
		#self.encoding_length = self._get_encoding_length()
		self.encoding = self._get_encoding()
		self.header_length = self.encoding_length + 18 ## See class docstring for explanation
		self._get_r_versions()


	def parse_data(
		self: Self,
		tabs: Optional[int] = None
	) -> None:
		"""
		Docstring
		"""
		cursor = self.header_length

		self.data = []

		while cursor < len(self.xdr_hex) and not self.hit_commands:
			parser = SEXPTYPE_Parser.get_sexptype_parser(
				self._get_hex_bytes(cursor, 4), cursor
			)

			obj, cursor = parser.parse(self, tabs = tabs)

			self.data.append(obj)

			#print(f"Top-level objects parsed: {len(self.data)}. Cursor is at {cursor}")


	def add_to_cache(
		self: Self,
		name: str
	) -> None:
		"""
		Add a named object to the cache so that its properties can be
		referenced at future instances. 
		"""
		curr_keys = list(self.char_cache.keys())

		if len(curr_keys) == 0:
			key = 1
		else:
			key = max(curr_keys) + 1

		self.char_cache[key] = name


class TypeNotImplementedError(NotImplementedError):
	def __init__(
		self: Self,
		sexptype_parser: "SEXPTYPE_Parser"
	) -> None:
		super().__init__(
			(
				f"Parsing for SEXPTYPE {sexptype_parser.__class__.__name__} (code {sexptype_parser.get_code()}) "
				f"at byte {sexptype_parser.cursor} not yet implemented."
			)
		)


## Parser methods
class SEXPTYPE_Parser:
	cursor: int
	orig_header: int

	## https://cran.r-project.org/doc/manuals/r-release/R-ints.pdf
	NILSXP = 0 			## NULL
	SYMSXP = 1 			## symbols
	LISTSXP = 2 		## pairlists
	CLOSXP = 3 			## closures
	ENVSXP = 4 			## environments
	PROMSXP = 5 		## promises
	LANGSXP = 6 		## language objects
	SPECIALSXP = 7 		## special functions
	BUILTINSXP = 8 		## builtin functions
	CHARSXP = 9 		## internal character strings
	LGLSXP = 10 		## logical vectors
	INTSXP = 13			## integer vectors
	REALSXP = 14		## numeric vectors
	CPLXSXP = 15 		## complex vectors
	STRSXP = 16			## character vectors
	DOTSXP = 17 		## dot-dot-dot object
	ANYSXP = 18 		## make “any” args work
	VECSXP = 19 		## list (generic vector)
	EXPRSXP = 20 		## expression vector
	BCODESXP = 21 		## byte code
	EXTPTRSXP = 22 		## external pointer
	WEAKREFSXP = 23 	## weak reference
	RAWSXP = 24 		## raw vector
	S4SXP = 25 			## S4 classes not of simple type

	## https://github.com/wch/r-source/blob/79298c499218846d14500255efd622b5021c10ec/src/main/serialize.c#L680-L720
	REFSXP = 255 		## idk what these are
	NILVALUE_SXP = 254
	GLOBALENV_SXP = 253
	UNBOUNDVALUE_SXP = 252
	MISSINGARG_SXP = 251
	BASENAMESPACE_SXP = 250
	NAMESPACESXP = 249
	PACKAGESXP = 248
	PERSISTSXP = 247
	CLASSREFSXP = 246
	GENERICREFSXP = 245
	BCREPDEF = 244
	BCREPREF = 243
	EMPTYENV_SXP = 242
	BASEENV_SXP = 241
	ATTRLANGSXP = 240
	ATTRLISTSXP = 239
	ALTREP_SXP = 238

	def __init__(self, orig_header: int, cursor: int):
		self.orig_header = orig_header
		self.cursor = cursor + 4

	@classmethod
	def get_sexptype_parser(
		cls,
		hex_str: List[str],
		cursor: int
	) -> "SEXPTYPE_Parser":
		"""
		"""
		orig_header = int(''.join(hex_str), 16)
		code =  orig_header & 0x000000ff
		#code = int(''.join(hex_str), 16) & 0x0000001f

		match code:
			case cls.NILSXP:
				return SEXPTYPE_NILSXP(orig_header, cursor)
			case cls.SYMSXP:
				return SEXPTYPE_SYMSXP(orig_header, cursor)
			case cls.LISTSXP:
				return SEXPTYPE_LISTSXP(orig_header, cursor)
			case cls.CLOSXP:
				return SEXPTYPE_CLOSXP(orig_header, cursor)
			case cls.ENVSXP:
				return SEXPTYPE_ENVSXP(orig_header, cursor)
			case cls.PROMSXP:
				return SEXPTYPE_PROMSXP(orig_header, cursor)
			case cls.LANGSXP:
				return SEXPTYPE_LANGSXP(orig_header, cursor)
			case cls.SPECIALSXP:
				return SEXPTYPE_SPECIALSXP(orig_header, cursor)
			case cls.BUILTINSXP:
				return SEXPTYPE_BUILTINSXP(orig_header, cursor)
			case cls.CHARSXP:
				return SEXPTYPE_CHARSXP(orig_header, cursor)
			case cls.LGLSXP:
				return SEXPTYPE_LGLSXP(orig_header, cursor)
			case cls.INTSXP:
				return SEXPTYPE_INTSXP(orig_header, cursor)
			case cls.REALSXP: 
				return SEXPTYPE_REALSXP(orig_header, cursor)
			case cls.CPLXSXP:
				return SEXPTYPE_CPLXSXP(orig_header, cursor)
			case cls.STRSXP:
				return SEXPTYPE_STRSXP(orig_header, cursor)
			case cls.DOTSXP:
				return SEXPTYPE_DOTSXP(orig_header, cursor)
			case cls.ANYSXP:
				return SEXPTYPE_ANYSXP(orig_header, cursor)
			case cls.VECSXP:
				return SEXPTYPE_VECSXP(orig_header, cursor)
			case cls.EXPRSXP:
				return SEXPTYPE_EXPRSXP(orig_header, cursor)
			case cls.BCODESXP:
				return SEXPTYPE_BCODESXP(orig_header, cursor)
			case cls.EXTPTRSXP:
				return SEXPTYPE_WEAKREFSXP(orig_header, cursor)
			case cls.WEAKREFSXP:
				return SEXPTYPE_RAWSXP(orig_header, cursor)
			case cls.RAWSXP:
				return SEXPTYPE_RAWSXP(orig_header, cursor)
			case cls.S4SXP:
				return SEXPTYPE_S4SXP(orig_header, cursor)
			case cls.REFSXP:
				return SEXPTYPE_REFSXP(orig_header, cursor)
			case cls.NILVALUE_SXP:
				return SEXPTYPE_NILVALUE_SXP(orig_header, cursor)
			case cls.GLOBALENV_SXP:
				return SEXPTYPE_GLOBALENV_SXP(orig_header, cursor)
			case cls.UNBOUNDVALUE_SXP:
				return SEXPTYPE_UNBOUNDVALUE_SXP(orig_header, cursor)
			case cls.MISSINGARG_SXP:
				return SEXPTYPE_MISSINGARG_SXP(orig_header, cursor)
			case cls.BASENAMESPACE_SXP:
				return SEXPTYPE_BASENAMESPACE_SXP(orig_header, cursor)
			case cls.NAMESPACESXP:
				return SEXPTYPE_NAMESPACESXP(orig_header, cursor)
			case cls.PACKAGESXP:
				return SEXPTYPE_PACKAGESXP(orig_header, cursor)
			case cls.PERSISTSXP:
				return SEXPTYPE_PERSISTSXP(orig_header, cursor)
			case cls.CLASSREFSXP:
				return SEXPTYPE_CLASSREFSXP(orig_header, cursor)
			case cls.GENERICREFSXP:
				return SEXPTYPE_GENERICREFSXP(orig_header, cursor)
			case cls.BCREPDEF:
				return SEXPTYPE_BCREPDEF(orig_header, cursor)
			case cls.BCREPREF:
				return SEXPTYPE_BCREPREF(orig_header, cursor)
			case cls.EMPTYENV_SXP:
				return SEXPTYPE_EMPTYENV_SXP(orig_header, cursor)
			case cls.BASEENV_SXP:
				return SEXPTYPE_BASEENV_SXP(orig_header, cursor)
			case cls.ATTRLANGSXP:
				return SEXPTYPE_ATTRLANGSXP(orig_header, cursor)
			case cls.ATTRLISTSXP:
				return SEXPTYPE_ATTRLISTSXP(orig_header, cursor)
			case cls.ALTREP_SXP:
				return SEXPTYPE_ALTREP_SXP(orig_header, cursor)

		raise ValueError(f"Got unhandled SEXPTYPE code {code}")


	@abstractmethod
	def parse(
		self: Self, 
		so: SeuratObjectRDS,
		tabs: Optional[int] = None
	) -> Tuple[Union[int, str, float, List, Dict, None], int]:
		pass

	def get_code(
		self: Self
	) -> int:
		#return getattr(self, self.__class__.__name__.split("_")[1])
		return getattr(self, '_'.join(self.__class__.__name__.split("_")[1:]))
	
	def tab_print_start(
		self: Self,
		cursor: int,
		tabs: Optional[int] = None
	) -> None:
		if tabs is not None:
			output = '  ' * tabs
			output += f"|-Parsing {type(self)} (code {self.get_code()}) at byte {cursor}"
			print(output)

	def tab_print(
		self: Self,
		msg: str,
		tabs: Optional[int] = None
	) -> None:
		if tabs is not None:
			output = '  ' * tabs
			output += msg
			print(output)

	def get_attr(
		self: Self,
		so: SeuratObjectRDS, 
		cursor: int,
		tabs: Optional[int] = None
	) -> Tuple[List, int]:
		"""
		"""
		new_tabs = tabs + 1 if tabs is not None else None

		attrs = []

		has_attr = (self.orig_header & (1 << 9)) >> 9

		new_cursor = cursor

		if has_attr:
			while True:
				next_parser = self.get_sexptype_parser(	
					so._get_hex_bytes(new_cursor, 4), new_cursor
				)

				if isinstance(next_parser, SEXPTYPE_NILVALUE_SXP):
					break

				attr, new_cursor = next_parser.parse(so, tabs = new_tabs)

				attrs.append(attr)

		return attrs, new_cursor


class SEXPTYPE_NILSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		self.tab_print_start(self.cursor, tabs)

		return None, self.cursor + 4


class SEXPTYPE_SYMSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		self.tab_print_start(self.cursor, tabs)
		new_tabs = tabs + 1 if tabs is not None else None

		new_cursor = self.cursor

		name, new_cursor = self.get_sexptype_parser(
			so._get_hex_bytes(new_cursor, 4), new_cursor
		).parse(so, new_tabs)
		self.tab_print(f"|-SYMSXP name is '{name}'", tabs = new_tabs)

		so.add_to_cache(name)

		return name, new_cursor


class SEXPTYPE_LISTSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		self.tab_print_start(self.cursor, tabs)
		new_tabs = tabs + 1 if tabs is not None else None

		new_cursor = self.cursor

		self.tab_print(f"|-LISTSXP parsing name.", tabs = new_tabs)
		list_name_parser = self.get_sexptype_parser(
			so._get_hex_bytes(new_cursor, 4), new_cursor
		)

		list_name, new_cursor = list_name_parser.parse(so, new_tabs)

		## I'm giving up
		if list_name == "commands":
			so.hit_commands = True
			return {list_name: {"val": None, "attr": None}}, new_cursor
			#return [list_name, ["val", None], ["attr", None]], new_cursor

		
		self.tab_print(f"|-LISTSXP parsing cdr in list '{str(list_name)[:100]}...'", tabs = new_tabs)
		next_parser = self.get_sexptype_parser(
			so._get_hex_bytes(new_cursor, 4), new_cursor
		)

		obj, new_cursor = next_parser.parse(so, new_tabs)

		self.tab_print(f"|-LISTSXP Checking attributes", tabs = new_tabs)
		attrs, new_cursor = self.get_attr(so, new_cursor, new_tabs)

		try:
			return {list_name: {"val": obj, "attr": attrs}}, new_cursor
		except TypeError:
			print("Unhashable list name")
			print(self.cursor)
			print(str(list_name)[:100]+"...")
			print(so.xdr_hex[self.cursor-4:self.cursor+200])
			sys.exit(1)


class SEXPTYPE_CLOSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_ENVSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_PROMSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_LANGSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_SPECIALSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_BUILTINSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_CHARSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		self.tab_print_start(self.cursor, tabs)
		new_tabs = tabs + 1 if tabs is not None else None

		new_cursor = self.cursor

		n_chars = so._get_int_from_hex(so._get_hex_bytes(new_cursor, 4))
		self.tab_print(f"|-CHARSXP Character has {n_chars} characters", tabs = new_tabs)
		new_cursor += 4

		char_s = so._get_chars_from_hex(so._get_hex_bytes(new_cursor, n_chars))
		self.tab_print(f"|-CHARSXP Character is '{char_s}'", tabs = new_tabs)

		return char_s, new_cursor + len(char_s)


class SEXPTYPE_LGLSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		self.tab_print_start(self.cursor, tabs)
		new_tabs = tabs + 1 if tabs is not None else None

		new_cursor = self.cursor

		n_bools = so._get_int_from_hex(so._get_hex_bytes(new_cursor, 4))
		self.tab_print(f"|-LGLSXP Logical vector has {n_bools} values", tabs = new_tabs)
		new_cursor += 4

		bool_l = []

		for i in range(n_bools):
			bool_l.append(bool(so._get_int_from_hex(so._get_hex_bytes(new_cursor, 4))))

			new_cursor += 4

		self.tab_print(f"|-LGLSXP First values are {','.join(map(str, bool_l[:5]))}...", tabs = new_tabs)

		self.tab_print(f"|-LGLSXP Checking attributes", tabs = new_tabs)
		attrs, new_cursor = self.get_attr(so, new_cursor, new_tabs)

		return {"val": bool_l, "attr": attrs}, new_cursor


class SEXPTYPE_INTSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		self.tab_print_start(self.cursor, tabs)
		new_tabs = tabs + 1 if tabs is not None else None

		new_cursor = self.cursor

		n_ints = so._get_int_from_hex(so._get_hex_bytes(new_cursor, 4))
		self.tab_print(f"|-INTSXP Integer vector has {n_ints} values", tabs = new_tabs)
		new_cursor += 4

		int_l = []

		for i in range(n_ints):
			int_l.append(so._get_int_from_hex(so._get_hex_bytes(new_cursor, 4)))

			new_cursor += 4

		self.tab_print(f"|-INTSXP First values are {','.join(map(str, int_l[:5]))}...", tabs = new_tabs)

		self.tab_print(f"|-INTSXP Checking attributes", tabs = new_tabs)
		attrs, new_cursor = self.get_attr(so, new_cursor, new_tabs)

		return {"val": int_l, "attr": attrs}, new_cursor


class SEXPTYPE_REALSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		self.tab_print_start(self.cursor, tabs)
		new_tabs = tabs + 1 if tabs is not None else None

		new_cursor = self.cursor

		n_doubles = so._get_int_from_hex(so._get_hex_bytes(new_cursor, 4))
		self.tab_print(f"|-REALSXP contains {n_doubles} values", tabs = new_tabs)
		new_cursor += 4

		doubles = []

		for i in range(n_doubles):
			doubles.append(struct.unpack('>d', bytearray.fromhex(''.join(so._get_hex_bytes(new_cursor, 8))))[0])
			new_cursor += 8

		self.tab_print(f"|-REALSXP First values are {','.join(map(lambda x: str(round(x, 2)), doubles[:5]))}...", tabs = new_tabs)

		self.tab_print(f"|-REALSXP Checking attributes", tabs = new_tabs)
		attrs, new_cursor = self.get_attr(so, new_cursor, new_tabs)

		return {"val": doubles, "attr": attrs}, new_cursor


class SEXPTYPE_CPLXSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_STRSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		self.tab_print_start(self.cursor, tabs)
		new_tabs = tabs + 1 if tabs is not None else None

		new_cursor = self.cursor

		n_char_vecs = so._get_int_from_hex(so._get_hex_bytes(new_cursor, 4))
		self.tab_print(f"|-STRSXP contains {n_char_vecs} character vectors", tabs = new_tabs)
		new_cursor += 4

		char_vecs = []

		for i in range(n_char_vecs):
			char_vec, new_cursor = self.get_sexptype_parser(
				so._get_hex_bytes(new_cursor, 4), new_cursor
			).parse(so, tabs = new_tabs)

			char_vecs.append(char_vec)

		return char_vecs, new_cursor


class SEXPTYPE_DOTSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_ANYSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_VECSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		self.tab_print_start(self.cursor, tabs)
		new_tabs = tabs + 1 if tabs is not None else None

		new_cursor = self.cursor

		n_items = so._get_int_from_hex(so._get_hex_bytes(new_cursor, 4))
		self.tab_print(f"|-VECSXP contains {n_items} items", tabs = new_tabs)
		new_cursor += 4

		items = []

		while len(items) < n_items:
			next_parser = self.get_sexptype_parser(
				so._get_hex_bytes(new_cursor, 4), new_cursor
			)

			if isinstance(next_parser, SEXPTYPE_NILVALUE_SXP):
				new_cursor += 4
				continue
			else:
				item, new_cursor = next_parser.parse(so, tabs = new_tabs)
				items.append(item)

		return items, new_cursor


class SEXPTYPE_EXPRSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		self.tab_print_start(self.cursor, tabs)
		new_tabs = tabs + 1 if tabs is not None else None

		new_cursor = self.cursor

		n_items = so._get_int_from_hex(so._get_hex_bytes(new_cursor, 4))
		self.tab_print(f"|-EXPRSXP contains {n_items} items", tabs = new_tabs)
		new_cursor += 4

		items = []

		for i in range(n_items):
			self.tab_print(f"|-Trying to interpret element at starting byte {new_cursor}", tabs = new_tabs)

			item, new_cursor = self.get_sexptype_parser(
				so._get_hex_bytes(new_cursor, 4), new_cursor
			).parse(so, tabs = new_tabs)

			self.tab_print(f"|-Got item {item} from starting byte {new_cursor}", tabs = new_tabs)

			items.append(item)

		return items, new_cursor


class SEXPTYPE_BCODESXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_EXTPTRSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_WEAKREFSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_RAWSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_S4SXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		self.tab_print_start(self.cursor, tabs)
		new_tabs = tabs + 1 if tabs is not None else None

		new_cursor = self.cursor

		data = []

		last_was_null = False

		while not so.hit_commands:
			next_parser = self.get_sexptype_parser(
				so._get_hex_bytes(new_cursor, 4), new_cursor
			)

			if isinstance(next_parser, SEXPTYPE_NILVALUE_SXP):
				if last_was_null:
					self.tab_print(
						f"|-S4SXP consecutive NIL at byte {new_cursor}, ending S4SXP", tabs = new_tabs
					)
					break

				last_was_null = True
				new_cursor += 4
				continue

			else:
				last_was_null = False

			element, new_cursor = next_parser.parse(
				so,
				tabs = new_tabs
			)

			data.append(element)

			self.tab_print(
				f"|-S4SXP Added element {len(data)}", tabs = new_tabs
			)

		return data, new_cursor


class SEXPTYPE_REFSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		self.tab_print_start(self.cursor, tabs)
		new_tabs = tabs + 1 if tabs is not None else None

		new_cursor = self.cursor

		name_key = self.orig_header >> 8
		try:
			name = so.char_cache[name_key]
		except:
			print(name_key)
			print(so.char_cache)
			exit(1)
		self.tab_print(f"|-REFSXP Cached symbols is '{name}' at key {name_key}", tabs = new_tabs)

		return name, new_cursor


class SEXPTYPE_NILVALUE_SXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		self.tab_print_start(self.cursor, tabs)

		return None, self.cursor + 4


class SEXPTYPE_GLOBALENV_SXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_UNBOUNDVALUE_SXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_MISSINGARG_SXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_BASENAMESPACE_SXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_NAMESPACESXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_PACKAGESXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_PERSISTSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_CLASSREFSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_GENERICREFSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_BCREPDEF(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_BCREPREF(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_EMPTYENV_SXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_BASEENV_SXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_ATTRLANGSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_ATTRLISTSXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		raise TypeNotImplementedError(self)


class SEXPTYPE_ALTREP_SXP(SEXPTYPE_Parser):
	def parse(self, so, tabs = None):
		#print(so.xdr_hex[self.cursor-4:self.cursor+50])

		## Try to just parse at the next byte and see what happens?? 
		self.tab_print_start(self.cursor, tabs)
		new_tabs = tabs + 1 if tabs is not None else None

		new_cursor = self.cursor

		## Skip to the name of the alt class (?)
		while True:
			cursor_byte = so._get_int_from_hex(so._get_hex_bytes(new_cursor, 4))

			if (cursor_byte == 0x00040009) or (cursor_byte & 0xff == 0xff):
				next_parser = self.get_sexptype_parser(
					so._get_hex_bytes(new_cursor, 4), new_cursor
				)

				alt_class_name, new_cursor = next_parser.parse(so, tabs = new_tabs)
				self.tab_print(f"|-ALTREP alt class name is {alt_class_name}", tabs = new_tabs)

				break

			new_cursor += 4

		so.add_to_cache(alt_class_name)
		if "base" not in so.char_cache.values():
			so.add_to_cache("base")

		if alt_class_name == "wrap_integer":
			while so._get_int_from_hex(so._get_hex_bytes(new_cursor, 4)) != 0xfe:
				new_cursor += 4
			new_cursor += 8 ## get passed the nil and also the list without a name

			next_parser = self.get_sexptype_parser(
				so._get_hex_bytes(new_cursor, 4), new_cursor
			)		

			obj, new_cursor = next_parser.parse(so, tabs = new_tabs)

			return obj, new_cursor

		if alt_class_name == "wrap_real":
			while so._get_int_from_hex(so._get_hex_bytes(new_cursor, 4)) != 0xfe:
				new_cursor += 4
			new_cursor += 8

			next_parser = self.get_sexptype_parser(
				so._get_hex_bytes(new_cursor, 4), new_cursor
			)

			return next_parser.parse(so, tabs = new_tabs)


		else:
			print(so.xdr_hex[self.cursor-64:self.cursor+64])
			raise ValueError(f"Unhandled alt class {alt_class_name} at byte {self.cursor}")


if __name__ == "__main__":
	so = SeuratObjectRDS("seurat_preprocessed_dataset.clustered.rds", debug_bytes = 256)
	so.load_tokens()
	#print(''.join(so.xdr_hex[18:18+15]))
	print(so.xdr_hex)
	#so.parse()



