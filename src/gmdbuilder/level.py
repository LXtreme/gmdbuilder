"""Level loading and exporting for Geometry Dash."""

from pathlib import Path
from typing import Iterator
from questionary import confirm
from gmdkit.models.level import Level as KitLevel

from gmdbuilder.object_types import ObjectList, ObjectType
from gmdbuilder.core import from_raw_object, to_raw_object


tag_group = 9999
_kit_level: KitLevel | None = None
_source_file: Path | None = None

def from_file(file_path: str | Path) -> None:
    """Load level from .gmd file into the module-level objects list."""
    global objects, _kit_level, _source_file
    
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Level file not found: {file_path}")
    
    _kit_level = KitLevel.from_file(str(path))
    _source_file = path
    
    objects = ObjectList()
    for kit_obj in _kit_level.objects:
        obj = from_raw_object(kit_obj)
        objects.append(obj)


class next():
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
    
    def _next(cls, iterator: Iterator[int], id_type: str) -> int:
        if not cls._initialized:
            cls._register_free_ids()
        try:
            return next(iterator)
        except StopIteration:
            raise RuntimeError(f"No free {id_type} IDs available")
    
    @classmethod
    def group(cls, count: int = 1) -> tuple[int,...]:
        """Get next free group ID (1-9999)."""
        return (cls._get_next(cls._group_iter, "group") for _ in range(count))
    
    @classmethod
    def item(cls, count: int = 1) -> tuple[int,...]:
        """Get next free item ID (1-9999)."""
        return (cls._get_next(cls._item_iter, "item") for _ in range(count))
    
    @classmethod
    def color(cls, count: int = 1) -> tuple[int,...]:
        """Get next free color ID (1-9999)."""
        return (cls._get_next(cls._color_iter, "color") for _ in range(count))
    
    @classmethod
    def collision(cls, count: int = 1) -> tuple[int,...]:
        """Get next free collision block ID (1-9999)."""
        return (cls._get_next(cls._collision_iter, "collision") for _ in range(count))
    
    @classmethod
    def control(cls, count: int = 1) -> tuple[int,...]:
        """Get next free control ID (1-9999)."""
        return (cls._get_next(cls._control_iter, "control") for _ in range(count))
    
    @classmethod
    def reset_all(cls):
        """Reset and rescan level objects. Call after significant object changes."""
        
        cls._initialized = False
        cls._group_iter = None
        cls._item_iter = None
        cls._color_iter = None
        cls._collision_iter = None
        cls._control_iter = None
    

def export(file_path: str | Path | None = None) -> None:
    """Export level to .gmd file."""
    global objects, _kit_level, _source_file
    
    if _kit_level is None:
        raise RuntimeError("No level loaded. Use level.from_file() first")
    
    if file_path is None:
        if _source_file is None:
            raise RuntimeError("No export path available. Provide file_path argument")
        
        if confirm("Overwrite the source file?", default=False).ask() is False:
            raise RuntimeError("Export cancelled by user")
        
        export_path = _source_file
    else:
        export_path = Path(file_path)
    
    # TODO: Run export validation here
    # validation.run_export_checks(objects)
    
    # TODO: Assign tag_group to new objects here
    # _assign_tag_groups(objects)
    
    from gmdkit.models.object import ObjectList as KitObjectList, Object as KitObject
    
    kit_objects = KitObjectList()
    for obj in objects:
        raw_dict = to_raw_object(obj)
        kit_obj = KitObject(raw_dict)
        kit_objects.append(kit_obj)
    
    # Update level objects
    _kit_level.objects = kit_objects
    _kit_level.to_file(str(export_path))