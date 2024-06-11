from pathlib import Path
from typing import Optional, TYPE_CHECKING, Type

from mcdreforged.constants import plugin_constant
from mcdreforged.plugin.type.directory_plugin import DirectoryPlugin, LinkedDirectoryPlugin
from mcdreforged.plugin.type.packed_plugin import PackedPlugin
from mcdreforged.plugin.type.regular_plugin import RegularPlugin
from mcdreforged.plugin.type.solo_plugin import SoloPlugin
from mcdreforged.utils import string_util, file_util
from mcdreforged.utils.types.path_like import PathLike

if TYPE_CHECKING:
	from mcdreforged.plugin.plugin_manager import PluginManager


def __get_plugin_class_from_path(file_path: PathLike, allow_disabled: bool) -> Optional[Type[RegularPlugin]]:
	file_path = Path(file_path)
	if file_path.is_file():
		if file_path.name.endswith(plugin_constant.DISABLED_PLUGIN_FILE_SUFFIX) and allow_disabled:
			file_path = file_path.parent / string_util.remove_suffix(file_path.name, plugin_constant.DISABLED_PLUGIN_FILE_SUFFIX)
		suffix = file_util.get_file_suffix(file_path)
		if suffix == plugin_constant.SOLO_PLUGIN_FILE_SUFFIX:  # .py
			return SoloPlugin
		if suffix in plugin_constant.PACKED_PLUGIN_FILE_SUFFIXES:  # .mcdr, .pyz
			return PackedPlugin
	elif file_path.is_dir() and (allow_disabled or not file_path.name.endswith(plugin_constant.DISABLED_PLUGIN_FILE_SUFFIX)):
		# directory plugins are not valid python modules
		if not (file_path / '__init__.py').is_file():
			if (file_path / plugin_constant.PLUGIN_META_FILE).is_file():
				return DirectoryPlugin
			elif (file_path / plugin_constant.LINK_DIRECTORY_PLUGIN_FILE_NAME).is_file():
				return LinkedDirectoryPlugin
	return None


def __maybe_plugin(file_path: PathLike, *, allow_disabled: bool) -> bool:
	return __get_plugin_class_from_path(file_path, allow_disabled) is not None


def is_plugin(file_path: PathLike) -> bool:
	return __maybe_plugin(file_path, allow_disabled=False)


def is_disabled_plugin(file_path: PathLike) -> bool:
	return not __maybe_plugin(file_path, allow_disabled=False) and __maybe_plugin(file_path, allow_disabled=True)


def create_regular_plugin(plugin_manager: 'PluginManager', file_path: PathLike) -> RegularPlugin:
	file_path = Path(file_path)
	cls = __get_plugin_class_from_path(file_path, False)
	if cls is None:
		raise TypeError('Trying to create a regular plugin with invalid path {}'.format(file_path))
	return cls(plugin_manager, file_path)
