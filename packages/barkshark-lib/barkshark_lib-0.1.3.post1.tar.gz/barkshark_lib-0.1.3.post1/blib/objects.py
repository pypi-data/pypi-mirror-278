import asyncio
import inspect
import traceback

from collections.abc import Awaitable, Callable
from typing import Any

from .misc import is_loop_running

try:
	from typing import Self

except ImportError:
	from typing_extensions import Self


SignalCallback = Callable[..., Awaitable[bool | None]]
MainSignalCallback = Callable[..., Awaitable[None]]


class Signal(list[SignalCallback]):
	"Allows a series of callbacks to get called via async. Use as a decorator for the base function."

	def __init__(self, timeout: float | int = 5.0):
		"""
			:param timeout: Time in seconds to wait before cancelling the callback
		"""

		self.timeout: float | int = timeout
		self.callback: MainSignalCallback | None = None
		self.object: Any = None


	def __get__(self, obj: Any, objtype: type[Any]) -> Self:
		if obj and not self.object:
			self.object = obj

		return self


	def __call__(self, callback: MainSignalCallback) -> Self:
		if not inspect.iscoroutinefunction(callback):
			raise RuntimeError(f"Not a coroutine: {callback.__name__}")

		self.callback = callback

		self.__doc__ = callback.__doc__
		self.__annotations__ = callback.__annotations__

		return self


	def append(self, value: SignalCallback) -> None:
		"""
			Add a callback

			:param value: Callback
		"""

		self.connect(value)


	def remove(self, value: SignalCallback) -> None:
		"""
			Remove a callback

			:param value: Callback
		"""

		self.disconnect(value)


	def emit(self, *args: Any, **kwargs: Any) -> None:
		"""
			Call all of the callbacks in the order they were added as well as the associated
			function.

			If any callback returns `True`, all other callbacks get skipped.

			:param args: Positional arguments to pass to all of the callbacks
			:param kwargs: Keyword arguments to pass to all of the callbacks
		"""

		if not is_loop_running():
			raise RuntimeError("Event loop is not running")

		asyncio.create_task(self.handle_emit(*args, **kwargs))


	def connect(self, callback: SignalCallback) -> SignalCallback:
		"""
			Add a function to the list of callbacks. Can be used as a decorator.

			:param callback: A callable or coroutine
		"""

		if callback not in self:
			list.append(self, callback)

		return callback


	def disconnect(self, callback: SignalCallback) -> None:
		"""
			Remove a function from the list of callbacks

			:param callback: A callable or coroutine
		"""

		if not self.callback:
			# oh boy something really goofed
			return

		try:
			list.remove(self, callback)

		except ValueError:
			cbname = callback.__name__
			signame = self.callback.__name__
			print(f"WARNING: '{cbname}' was not connted to signal '{signame}'")


	async def handle_emit(self, *args: Any, catch_errors: bool = True, **kwargs: Any) -> None:
		"""
			This gets called by :meth:`Signal.emit` as an :class:`asyncio.Task`.

			:param args: Positional arguments to pass to all of the callbacks
			:param kwargs: Keyword arguments to pass to all of the callbacks
			:param catch_errors: Whether or not to handle exceptions raised from callbacks
		"""

		if not self.callback:
			# oh boy something really goofed
			return

		for callback in self:
			try:
				if await self.handle_callback(callback, *args, **kwargs):
					break

			except Exception:
				if not catch_errors:
					raise

				traceback.print_exc()
				break

		try:
			await self.handle_callback(self.callback, *args, **kwargs)

		except Exception:
			if not catch_errors:
				raise

			traceback.print_exc()


	async def handle_callback(self,
							callback: Callable[..., Awaitable[bool | None]],
							*args: Any,
							**kwargs: Any) -> bool | None:

		try:
			# asyncio.timeout and asyncio.wait_for complain, so need to find a new way
			# async with asyncio.timeout(self.timeout):
			if args and args[0] == self.object:
				return await callback(*args, **kwargs)

			else:
				return await callback(self.object, *args, **kwargs)

		except TimeoutError:
			print(f"Callback '{callback.__name__}' timed out")
			return True



class Object:
	"Enhanced :class:`object` with a :class:`Signal` for attribute setting"

	@Signal(5.0)
	async def notify(self, key: str, value: Any) -> None:
		"""
			:class:`blib.Signal` that gets emitted when a property has been set

			:param key: Name of the property
			:param value: New property that has been set
		"""


	def __setattr__(self, key: str, value: Any) -> None:
		object.__setattr__(self, key, value)

		if is_loop_running():
			self.notify.emit(key, value)
