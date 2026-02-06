"""Level loading and exporting for Geometry Dash."""

from pathlib import Path
from typing import Iterator
from gmdbuilder.object_typeddict import ObjectType
from questionary import confirm
from gmdkit.models.level import Level as KitLevel
from gmdkit.models.object import ObjectList as KitObjectList, Object as KitObject
from gmdkit.extra.live_editor import WEBSOCKET_URL, LiveEditor
from gmdkit.serialization import type_cast as tc
from gmdkit.casting.object_props import PROPERTY_DECODERS, PROPERTY_ENCODERS # type: ignore

from gmdbuilder.object_types import ObjectList
from gmdbuilder.mappings.obj_prop import ObjProp
from gmdbuilder.core import from_raw_object, to_raw_object


RAW_DECODERS = {}
for key, decoder in PROPERTY_DECODERS.items():
    # Keep basic types as-is
    if decoder in (tc.to_bool, int, float):
        RAW_DECODERS[key] = decoder
    else:
        RAW_DECODERS[key] = str

RAW_ENCODERS = {}
for key, encoder in PROPERTY_ENCODERS.items(): # type: ignore
    if encoder in (tc.from_bool, tc.from_float):
        RAW_ENCODERS[key] = encoder
    else:
        RAW_ENCODERS[key] = str


class RawObject(KitObject):
    DECODER = staticmethod(tc.dict_cast(RAW_DECODERS, numkey=True)) # type: ignore
    ENCODER = staticmethod(tc.dict_cast(RAW_ENCODERS, default=tc.serialize)) # type: ignore

class RawObjectList(KitObjectList):
    DECODER = RawObject.from_string # type: ignore
    ENCODER = staticmethod(lambda obj: obj.to_string()) # type: ignore



objects = ObjectList(live_editor=False)
"""List of level's objects."""
tag_group = 9999
"""Deletes all objects with this group and adds this group to new added objects"""
_kit_level: KitLevel | None = None
_source_file: Path | None = None
_live_editor_connected = False

def from_file(file_path: str | Path) -> None:
    """Load level from .gmd file into the module-level objects list."""
    global objects, tag_group, _kit_level, _source_file, _live_editor_connected
    
    if _source_file is not None or _live_editor_connected:
        raise RuntimeError("FORBIDDEN: Level file is loaded! Loading multiple levels at once overrides global state")
    
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Level file not found: {file_path=}")
    
    _kit_level = KitLevel.from_file(path) # type: ignore
    _source_file = path
    objects = ObjectList(live_editor=False)
    
    for raw_obj in _kit_level.objects: # type: ignore
        obj = from_raw_object(raw_obj, bypass_validation=True) # type: ignore
        if tag_group not in obj.get(ObjProp.GROUPS, set()): # type: ignore
            objects.append(obj, bypass_validation=True, import_mode=True) # type: ignore


def from_live_editor(url: str = WEBSOCKET_URL) -> None:
    global objects, tag_group, _kit_level, _source_file, _live_editor_connected
    
    if _source_file is not None or _live_editor_connected:
        raise RuntimeError("FORBIDDEN: Level file is loaded! Loading multiple levels at once overrides global state")
    
    objects = ObjectList(live_editor=True)
    _kit_level = LiveEditor(url) # type: ignore
    _kit_level.connect() # type: ignore
    _kit_level.remove_object_group(tag_group) # type: ignore
    _, kit_objects = _kit_level.get_level_string() # type: ignore
    
    for raw_obj in kit_objects: # type: ignore
        objects.append(from_raw_object(raw_obj), bypass_validation=True) # type: ignore
    
    _live_editor_connected = True


class new():
    """Return the next free ID for group, item, color, collision, control IDs."""
    _initialized = False
    _group_iter: Iterator[int] | None = None
    _item_iter: Iterator[int] | None = None
    _color_iter: Iterator[int] | None = None
    _collision_iter: Iterator[int] | None = None
    _control_iter: Iterator[int] | None = None
    
    @classmethod
    def _register_free_ids(cls):
        cls._initialized = True
        global objects
        
        cls._used_group_ids: set[int] = set()
        cls._used_item_ids: set[int] = set()
        cls._used_color_ids: set[int] = set()
        cls._used_collision_ids: set[int] = set()
        cls._used_control_ids: set[int] = set()
        
        for obj in objects:
            if (key := ObjProp.GROUPS) in obj:
                cls._used_group_ids.update(obj[key])
            if (key := ObjProp.Trigger.Count.ITEM_ID) in obj:
                cls._used_item_ids.add(int(obj[key]))
            if (key := ObjProp.Trigger.CollisionBlock.BLOCK_ID) in obj:
                cls._used_collision_ids.add(int(obj[key]))
            if (key := ObjProp.Trigger.CONTROL_ID) in obj:
                cls._used_control_ids.add(int(obj[key]))
        
        cls._group_iter = (i for i in range(1, 9999) if i not in cls._used_group_ids)
        cls._item_iter = (i for i in range(1, 9999) if i not in cls._used_item_ids)
        # cls._color_iter = (i for i in range(1, 9999) if i not in cls._used_color_ids)
        cls._collision_iter = (i for i in range(1, 9999) if i not in cls._used_collision_ids)
        cls._control_iter = (i for i in range(1, 9999) if i not in cls._used_control_ids)
    
    
    @classmethod
    def _get_next(cls, iterator: Iterator[int] | None, id_type: str) -> int:
        if not cls._initialized:
            cls._register_free_ids()
        if iterator is None:
            raise RuntimeError(f"Iterator for {id_type} IDs is not initialized")
        try:
            return next(iterator)
        except StopIteration:
            raise RuntimeError(f"No free {id_type} IDs available")
    
    @classmethod
    def group(cls) -> int:
        """Get next free group ID (1-9999)."""
        return cls._get_next(cls._group_iter, "group")
    
    @classmethod
    def item(cls) -> int:
        """Get next free item ID (1-9999)."""
        return cls._get_next(cls._item_iter, "item")
    
    @classmethod
    def color(cls) -> int:
        """Get next free color ID (1-9999)."""
        return cls._get_next(cls._color_iter, "color")
    
    @classmethod
    def collision(cls) -> int:
        """Get next free collision block ID (1-9999)."""
        return cls._get_next(cls._collision_iter, "collision")
    
    @classmethod
    def control(cls) -> int:
        """Get next free control ID (1-9999)."""
        return cls._get_next(cls._control_iter, "control")
    
    @classmethod
    def group_multi(cls, count: int) -> tuple[int,...]:
        """Get next free group IDs (1-9999)."""
        return tuple(cls._get_next(cls._group_iter, "group") for _ in range(count))
    
    @classmethod
    def item_multi(cls, count: int) -> tuple[int,...]:
        """Get next free item IDs (1-9999)."""
        return tuple(cls._get_next(cls._item_iter, "item") for _ in range(count))
    
    @classmethod
    def color_multi(cls, count: int) -> tuple[int,...]:
        """Get next free color IDs (1-9999)."""
        return tuple(cls._get_next(cls._color_iter, "color") for _ in range(count))
    
    @classmethod
    def collision_multi(cls, count: int) -> tuple[int,...]:
        """Get next free collision block IDs (1-9999)."""
        return tuple(cls._get_next(cls._collision_iter, "collision") for _ in range(count))
    
    @classmethod
    def control_multi(cls, count: int) -> tuple[int,...]:
        """Get next free control IDs (1-9999)."""
        return tuple(cls._get_next(cls._control_iter, "control") for _ in range(count))
    
    @classmethod
    def reset_all(cls):
        """Reset and rescan level objects. Call after significant object changes."""
        cls._initialized = False
        cls._group_iter = None
        cls._item_iter = None
        cls._color_iter = None
        cls._collision_iter = None
        cls._control_iter = None
    

def _validate_and_prepare_objects(validated_objects: ObjectList) -> None:
    """Run validation and preparation checks on objects before export."""
    # TODO: Run export validation here
    # validation.run_export_checks(validated_objects)
    
    # TODO: Assign tag_group to new objects here
    # _assign_tag_groups(validated_objects)
    pass


def _objects_to_kit(validated_objects: list[ObjectType]) -> KitObjectList:
    """Convert ObjectList to gmdkit ObjectList."""
    
    kit_objects = KitObjectList()
    for obj in validated_objects:
        kit_objects.append(KitObject(to_raw_object(obj))) #type: ignore
    print(f"Exporting {len(kit_objects)} objects: \n{kit_objects!r}\n")
    return kit_objects


def export_to_file(file_path: str | Path | None = None) -> None:
    """Export level to .gmd file."""
    global objects, _kit_level, _source_file
    
    if _kit_level is None:
        raise RuntimeError("No level loaded. Use level.from_file() first")
    
    # Determine export path
    if file_path is None:
        if _source_file is None:
            raise RuntimeError("No export path available. Provide file_path argument")
        
        if confirm("Overwrite the source file?", default=False).ask() is False:
            raise RuntimeError("Export cancelled by user")
        export_path = _source_file
    else:
        export_path = Path(file_path)
    
    # Validate and prepare objects
    _validate_and_prepare_objects(objects)
    
    # Convert and export
    _kit_level.objects = objects #type: ignore
    _kit_level.to_file(str(export_path)) #type: ignore
    new.reset_all()
    objects.clear()


def export_to_live_editor(*, batch_size: int = 500) -> None:
    """Export level to live editor."""
    global objects, _kit_level, _live_editor_connected
    
    if not _live_editor_connected:
        raise RuntimeError("No live editor connection. Use level.from_live_editor() first")
    
    if _kit_level is None:
        raise RuntimeError("Live editor instance not found")
    
    # Validate and prepare objects
    _validate_and_prepare_objects(objects)
    
    kit_objects = _objects_to_kit(objects.added_objects)
    _kit_level.add_objects(kit_objects, batch_size) #type: ignore
    _kit_level.close() #type: ignore
    new.reset_all()
    objects.clear()