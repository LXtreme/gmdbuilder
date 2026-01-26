"""Level loading and exporting for Geometry Dash."""

from pathlib import Path
from typing import Any
from questionary import confirm
from gmdkit.models.level import Level as KitLevel

from gmdbuilder.object_types import ObjectList, ObjectType
from gmdbuilder.core import from_raw_object, to_raw_object


# Module-level state
objects: ObjectList = ObjectList()
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