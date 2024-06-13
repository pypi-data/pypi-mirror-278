from __future__ import annotations

import os
import shutil
import sys

from collections.abc import Iterator, Sequence
from glob import iglob

from .enums import FileType, XdgDir
from .errors import FileError
from .misc import FileSize

try:
	from typing import Self

except ImportError:
	from typing_extensions import Self


COMPRESSION_EXT = ("br", "bz2", "gz", "lz", "lz4", "lzma", "lzo", "rz", "sz", "xz", "z", "zst")


class Path(str):
	"Represents a path"

	def __init__(self, path: str, normalize: bool = False) -> None:
		"""
			Create a new ``Path`` object

			:param path: Path to manage
			:param normalize: Parse a path to remove unecessary and redundant segments
		"""


	def __new__(cls: type[Self], path: str, normalize: bool = False) -> Self:
		if normalize:
			path = os.path.normpath(path)

		return str.__new__(cls, path)


	def __repr__(self) -> str:
		return f"{self.__class__.__name__}('{str(self)}')"


	@property
	def ext(self) -> str:
		"Get the extension if one exists"
		parts = self.name.split(".")

		if len(parts) == 1:
			return ""

		if len(parts) == 2:
			return parts[1]

		if parts[-1].lower() in COMPRESSION_EXT:
			return ".".join(parts[-2:])

		return parts[-1]


	@property
	def name(self) -> str:
		"Return the last path segment"
		return os.path.basename(self)


	@property
	def parent(self) -> Self:
		"Remove the last path segment"
		return self.__class__(os.path.dirname(self))


	@property
	def stem(self) -> str:
		return self.name.rstrip(self.ext).rstrip(".")


	def join(self, *parts: str, normalize: bool = False) -> Self: # type: ignore[override]
		"""
			Append a path segment

			:param parts: Path segments to append
			:param normalize: Normalize the path before returning it
		"""
		return self.__class__(os.path.join(self, *parts), normalize = normalize)


	def normalize(self) -> Self:
		"Remove unecessary and redundant segments"
		return self.__class__(self, True)


class File(Path):
	"Represents a file on the local filesystem"

	exist_ok: bool = True
	"If ``True``, don't raise an exception when the file or directory does exist"

	missing_ok: bool = True
	"If ``True``, don't raise an exception when the file or directory doesn't exist"

	parents: bool = True
	"If ``True``, don't raise an exception when the parent directory doesn't exist"


	def __init__(self, path: str, normalize: bool = True) -> None:
		"""
			Create a new ``File`` object

			:param path: Path to the file or directory
			:param normalize: Parse a path to remove unecessary and redundant segments
		"""

		Path.__init__(self, path, normalize = normalize)


	@classmethod
	def cwd(cls: type[Self]) -> Self:
		"Create a new :class:`Path` from the current working directory"

		return cls(".").resolve()


	@classmethod
	def home(cls: type[Self]) -> Self:
		"Create a new :class:`Path` from the current user home directory"

		return cls("~").resolve()


	@classmethod
	def script(cls: type[Self]) -> Self:
		"Create a new :class:`Path` from the currently executed script"

		try:
			path = getattr(sys.modules["__main__"], "__file__")

		except Exception:
			path = sys.argv[0]

		return cls(path).resolve().parent


	@classmethod
	def xdg(cls: type[Self], dir_type: XdgDir) -> Self:
		"""
			Create a new :class:`Path` for an XDG directory

			:param dir_type: XDG name
		"""

		return cls(XdgDir.parse(dir_type).path)


	@property
	def exists(self) -> bool:
		"Check if the path exists"

		return os.path.exists(self)


	@property
	def isdir(self) -> bool:
		"Check if the path is a directory"

		return os.path.isdir(self)


	@property
	def isfile(self) -> bool:
		"Check if the path is a file"

		return os.path.isfile(self)


	@property
	def islink(self) -> bool:
		"Check if the path is a symlink"

		return os.path.islink(self)


	@property
	def isabsolute(self) -> bool:
		"Check if the path is absolute"

		return os.path.isabs(self)


	@property
	def size(self) -> FileSize:
		"Get the size of the path or directory"

		return FileSize(os.path.getsize(self))


	def get_types(self) -> tuple[FileType, ...]:
		"Get all the types of the path"

		types = []

		if self.isfile:
			types.append(FileType.FILE)

		elif self.isdir:
			types.append(FileType.DIR)

		else:
			types.append(FileType.UNKNOWN)

		if self.islink:
			types.append(FileType.LINK)

		return tuple(types)


	def glob(self,
			pattern: str = "**",
			recursive: bool = False,
			hidden: bool = False,
			ext: Sequence[str] | None = None) -> Iterator[File]:
		"""
			Iterate through a directory with paths matching a specific pattern

			.. note:: See :class:`glob.iglob` for pattern usage

			:param pattern: Filename pattern to match
			:param recursive: Whether or not to search through sub-directories
			:param hidden: List hidden files
			:param ext: Include only the specified extensions in the result if set
			:raises FileError: If the path is not a directory or does not exist
		"""

		if self.isfile:
			raise FileError.IsFile(self)

		if not self.exists:
			raise FileError.NotFound(self)

		for path in iglob(pattern, root_dir = self, recursive = recursive, include_hidden = hidden):
			filepath = self.join(path)

			if ext is None or filepath.ext in ext:
				yield filepath


	def mkdir(self, mode: int = 0o755) -> None:
		"""
			Create a directory and all parent directories

			.. note:: ``mode`` will eventually use a ``UnixPerm`` object. Use an octal
				(ex: ``0o755``) for now

			:param mode: Unix permission flags to set for the new directories
		"""

		os.makedirs(self, mode = mode, exist_ok = self.exist_ok)


	def remove(self) -> None:
		"Delete the file or directory"

		if self.islink or self.isfile:
			os.remove(self)

		elif not self.isdir:
			raise ValueError("File is not a file, directory, or symlink")

		if self.parents:
			shutil.rmtree(self)

		else:
			os.rmdir(self)


	def resolve(self) -> Self:
		"Replace `~` with the current user home and follow any symlinks in the path"

		path = str(self)

		if self.startswith("~"):
			path = os.path.expanduser(path)

		return type(self)(os.path.realpath(path, strict = False))


	def relative_to(self, path: Path) -> str:
		"""
			Get the a path segment relative to another path

			:param path: Path to use as the base directory
			:raises ValueError: When the path is not a child of the specified path
		"""

		if not self.startswith(path):
			raise ValueError("This path is not relative to the specified path")

		return self.replace(path if path.endswith("/") else f"{path}/", "")


	def symlink_from(self, src: File) -> None:
		"""
			Create a symlink at the current path from another path

			:param src: Path to link to
		"""

		src = src.resolve()
		os.symlink(src, self, target_is_directory = src.isdir)
