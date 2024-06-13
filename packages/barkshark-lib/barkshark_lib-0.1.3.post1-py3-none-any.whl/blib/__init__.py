__software__ = "Barkshark Lib"
__version_info__ = (0, 1, 3)
__version__ = ".".join(str(v) for v in __version_info__) + "-1"
__author__ = "Zoey Mae"
__homepage__ = "https://git.barkshark.xyz/barkshark/blib"


from .application import Application
from .transport import AsyncTransport

from .enums import (
	Enum,
	IntEnum,
	IntFlagEnum,
	StrEnum,
	FileSizeUnit,
	FileType,
	HttpMethod,
	HttpStatus,
	ProtocolPort,
	XdgDir
)

from .errors import (
	Error,
	ErrorCode,
	ErrorMeta,
	FileError
)

# todo: convert these errors to use the new Error class
from .errors import (
	HttpError

)

from .icon_theme import (
	FileIconTheme,
	Icon,
	IconTheme,
	IconThemes,
	MemoryIconTheme
)

from .misc import (
	catch_errors,
	convert_to_boolean,
	convert_to_bytes,
	convert_to_string,
	deprecated,
	get_object_name,
	get_object_properties,
	get_resource_path,
	get_top_domain,
	http_request,
	is_loop_running,
	random_str,
	time_function,
	time_function_pprint,
	DictProperty,
	Env,
	FileSize,
	HttpDate,
	JsonBase,
	NamedTuple,
	RunData,
	StaticProperty
)

from .objects import (
	Object,
	Signal
)

from .path import (
	File,
	Path
)

from .router import (
	Match,
	Route,
	Router
)

from .url import (
	Query,
	Url
)
