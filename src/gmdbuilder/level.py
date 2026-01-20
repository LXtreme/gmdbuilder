"""Type-safe level builder for Geometry Dash levels."""

from typing import Any, Callable
from pathlib import Path

from gmdbuilder.object import Object
from gmdbuilder.validation import export_validation
from gmdbuilder.kit_interface import (
    load_level_from_file,
    save_level_to_file,
    get_level_objects,
    set_level_objects,
    KitLevel,
)


class Level:
    """
    Type-safe GD level builder.
    
    Example:
        level = Level.from_file("level.gmd")
        obj = Object(1)
        obj[ObjProp.X] = 100
        level.add_object(obj)
        level.save("output.gmd")
    """
    
    def __init__(self):
        self._kit_level: KitLevel = KitLevel()
        self._objects: list[Object] = []
        self._loaded = False
    
    @classmethod
    def from_file(cls, file_path: str | Path) -> "Level":
        """Load level from .gmd file."""
        level = cls()
        level._kit_level = load_level_from_file(str(file_path))
        level._load_objects_from_kit()
        level._loaded = True
        return level
    
    @classmethod
    def from_save(cls, level_name: str) -> "Level":
        """Load level from GD save file. Not yet implemented."""
        raise NotImplementedError("Loading from save file not yet implemented")
    
    @classmethod
    def from_live_editor(cls) -> "Level":
        """Load from WSLiveEditor. Not yet implemented."""
        raise NotImplementedError("Live editor integration not yet implemented")
    
    def _load_objects_from_kit(self) -> None:
        """Internal: Load objects from kit level."""
        typed_objects = get_level_objects(self._kit_level)
        self._objects = [Object.from_dict(obj) for obj in typed_objects]
    
    def save(self, file_path: str | Path, *, validate: bool = True) -> None:
        """Save level to .gmd file."""
        if validate:
            self.validate()
        
        self._sync_objects_to_kit()
        save_level_to_file(self._kit_level, str(file_path))
    
    def save_to_live_editor(self) -> None:
        """Save to WSLiveEditor. Not yet implemented."""
        raise NotImplementedError("Live editor integration not yet implemented")
    
    def save_to_save_file(self, level_name: str) -> None:
        """Save to GD save file. Not yet implemented."""
        raise NotImplementedError("Saving to save file not yet implemented")
    
    def _sync_objects_to_kit(self) -> None:
        """Internal: Sync objects back to kit level."""
        typed_objects = [obj.properties for obj in self._objects]
        set_level_objects(self._kit_level, typed_objects)
    
    def add_object(self, obj: Object) -> None:
        """Add a single object to the level."""
        self._objects.append(obj)
    
    def add_objects(self, objects: list[Object]) -> None:
        """Add multiple objects to the level."""
        self._objects.extend(objects)
    
    def get_objects(self) -> list[Object]:
        """Get all objects in the level."""
        return self._objects.copy()
    
    def filter_objects(self, predicate: Callable[[Object], bool]) -> list[Object]:
        """Get objects matching a condition."""
        return [obj for obj in self._objects if predicate(obj)]
    
    def clear_objects(self) -> None:
        """Remove all objects from the level."""
        self._objects.clear()
    
    @property
    def object_count(self) -> int:
        """Get the number of objects in the level."""
        return len(self._objects)
    
    def validate(self) -> None:
        """Run all deferred validations. Raises ValidationError on failure."""
        export_validation(self)
    
    def get_property(self, key: int) -> Any:
        """Get a level property (name, description, etc). Use lvl_prop constants."""
        return self._kit_level.get(key)
    
    def set_property(self, key: int, value: Any) -> None:
        """Set a level property. Use lvl_prop constants."""
        self._kit_level[key] = value
    
    def __repr__(self) -> str:
        return f"Level(objects={len(self._objects)}, loaded={self._loaded})"
    
    def __len__(self) -> int:
        return len(self._objects)