"""Level loading and exporting for Geometry Dash."""

from pathlib import Path
from typing import Iterator
from questionary import confirm
from gmdkit.models.level import Level as KitLevel
from gmdkit.models.object import ObjectList as KitObjectList, Object as KitObject
from gmdkit.extra.live_editor import WEBSOCKET_URL, LiveEditor

from gmdbuilder.object_types import ObjectList
from gmdbuilder.mappings.obj_prop import ObjProp
from gmdbuilder.core import from_raw_object, kit_to_raw_obj, to_raw_object


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
    
    for kit_obj in _kit_level.objects: # type: ignore
        obj = from_raw_object(kit_to_raw_obj(kit_obj), bypass_validation=True) # type: ignore
        if tag_group not in obj.get(ObjProp.GROUPS, set()):
            objects.append(obj, bypass_validation=True)


def from_live_editor(url: str = WEBSOCKET_URL) -> None:
    global objects, _kit_level, _source_file, _live_editor_connected
    
    if _source_file is not None or _live_editor_connected:
        raise RuntimeError("FORBIDDEN: Level file is loaded! Loading multiple levels at once overrides global state")
    
    objects = ObjectList(live_editor=True)
    _kit_level = LiveEditor(url) # type: ignore
    _kit_level.connect() # type: ignore
    _, kit_objects = _kit_level.get_level_string() # type: ignore
    
    for kit_obj in kit_objects: # type: ignore
        obj = from_raw_object(kit_to_raw_obj(kit_obj), bypass_validation=True) # type: ignore
        if tag_group not in obj.get(ObjProp.GROUPS, set()):
            objects.append(obj, bypass_validation=True)
    
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
        ...
    
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


def _objects_to_kit(validated_objects: ObjectList) -> KitObjectList:
    """Convert ObjectList to gmdkit ObjectList."""
    
    kit_objects = KitObjectList()
    for obj in validated_objects:
        kit_objects.append(KitObject(to_raw_object(obj))) #type: ignore
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
    kit_objects = _objects_to_kit(objects)
    _kit_level.objects = kit_objects #type: ignore
    _kit_level.to_file(str(export_path)) #type: ignore
    new.reset_all()
    objects.clear()


def export_to_live_editor(*, batch_size: int = 500) -> None:
    """Export level to live editor."""
    global objects, _live_editor_connected
    
    if not _live_editor_connected:
        raise RuntimeError("No live editor connection. Use level.from_live_editor() first")
    
    # Validate and prepare objects
    _validate_and_prepare_objects(objects)
    
    # Convert and export
    kit_objects = _objects_to_kit(objects)
    LiveEditor.add_objects(kit_objects, batch_size) #type: ignore
    LiveEditor.close() #type: ignore
    new.reset_all()
    objects.clear()