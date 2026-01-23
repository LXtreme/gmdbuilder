"""
Internal bridge between gmdkit and gmdbuilder's type-safe interfaces.

NOT for end users. Only used internally by Object and Level classes.

TODO: Ask HDanke to split get_level_string into two methods:
    1. get_level_string() -> str (returns raw level string)
    2. get_level_objects() -> ObjectString (returns parsed ObjectString with .objects)
    
Currently get_level_string() calls self.load() which returns ObjectString, not a string.
"""

from typing import Any, TypeAlias

from gmdkit.models.level import Level as KitLevel  # type: ignore
from gmdkit.models.object import Object as KitObject, ObjectList as KitObjectList  # type: ignore
from gmdkit.extra.live_editor import LiveEditor  # type: ignore

from gmdbuilder.object_types import ObjectType

# Live editor connection state
_live_editor_connection: LiveEditor | None = None
_live_editor_connected = False

TypedObjectDict: TypeAlias = ObjectType

def typed_dict_to_raw(typed_obj: TypedObjectDict) -> dict[int, Any]:
    """Convert {"a1": val, "a2": val} to {1: val, 2: val}"""
    raw: dict[int, Any] = {}
    for key, value in typed_obj.items():
        if key.startswith('a') and len(key) > 1:
            raw[int(key[1:])] = value
        else:
            raise ValueError(f"Invalid typed key format: {key}")
    return raw


def load_level_from_file(file_path: str) -> KitLevel:
    """Load level from .gmd file"""
    return KitLevel.from_file(file_path)


def save_level_to_file(kit_level: KitLevel, file_path: str):
    """Save level to .gmd file"""
    kit_level.to_file(file_path)


def add_objects_to_level(kit_level: KitLevel, objects: KitObjectList):
    """Add objects to a level's object list"""
    for obj in objects:
        kit_level.objects.append(obj)


def add_objects_live(objects: KitObjectList, batch_size: int | None = None):
    """Add objects to live editor in real-time"""
    global _live_editor_connection, _live_editor_connected
    
    if not _live_editor_connected:
        raise RuntimeError("Live editor not connected. Call connect_live_editor() first")
    
    assert _live_editor_connection is not None
    _live_editor_connection.add_objects(objects, batch_size=batch_size)



def get_objects_from_live_editor() -> KitObjectList:
    """Load current level from WSLiveEditor
    
    NOTE: Pending gmdkit fix for get_level_string vs get_level_objects naming
    """
    global _live_editor_connection, _live_editor_connected
    if not _live_editor_connected or _live_editor_connection is None:
        raise RuntimeError("Live editor not connected. Call connect_live_editor() first")
    
    objects = _live_editor_connection.get_level_string()  # type: ignore
    return objects


WEBSOCKET_URL_DEFAULT = "ws://127.0.0.1:1313" # same default as gmdkit

def connect_live_editor(url: str | None = None):
    """Connect to WSLiveEditor"""
    global _live_editor_connection, _live_editor_connected
    
    _live_editor_connection = LiveEditor(url or WEBSOCKET_URL_DEFAULT)
    _live_editor_connection.connect()
    _live_editor_connected = True


def disconnect_live_editor() -> None:
    """Disconnect from WSLiveEditor"""
    global _live_editor_connection, _live_editor_connected
    
    if _live_editor_connection:
        _live_editor_connection.close()
    _live_editor_connection = None
    _live_editor_connected = False
