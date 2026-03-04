"""Level loading and exporting for Geometry Dash."""

from enum import IntEnum
import time

from pathlib import Path
from typing import Any, Callable, Iterable, Literal, SupportsIndex, overload

from gmdbuilder.fields import obj_id
from gmdkit.extra.live_editor import WEBSOCKET_URL, LiveEditor
from gmdkit.models.level import Level as KitLevel
from gmdkit.models.object import ObjectList as KitObjectList

from gmdbuilder.core import Object, from_kit_object, to_kit_object
from gmdbuilder.mappings import obj_prop
from gmdbuilder.object_types import ObjectType
from gmdbuilder.validation import get_trigger_targets, validate_target_exists

ObjectPatternMatch = dict[str, Any] | ObjectType | Callable[[ObjectType], bool]

class ObjectList(list[ObjectType]):
    """
    A list that validates ObjectType mutations.
    Only additions are allowed in live editor mode
    
    - append/insert/extend: wraps objects in ValidatedObject for runtime validation
    - Direct indexing (objects[i]): read-only access
    - Property edits (objects[i]['a2'] = x): validated by ValidatedObject.__setitem__
    - Addition operators (+, +=): disabled - use extend() instead
    """
    
    def __init__(self, *, live_editor: bool):
        super().__init__()
        self._live_editor_mode = live_editor
        self.added_objects: list[ObjectType] = []
    
    def delete_where(self, condition: ObjectPatternMatch, *, limit: int = -1) -> int:
        """
        Delete objects matching a condition (dict or predicate)
        
        Returns number of deleted objects.
        
        For dict-matching, dict must match standard ObjectType keys/values.
        'None' can be used as a wildcard value (not key).
        """
        if self._live_editor_mode:
            raise RuntimeError("Direct object deleting is not allowed in live editor mode")
        if limit < -1 or limit == 0:
            raise ValueError("delete_where limit must be -1 (no limit) or positive")
        
        predicate: Callable[[ObjectType], bool]
        if callable(condition):
            predicate = condition
        else:
            predicate = lambda obj: all(
                k in obj and (obj.get(k) == v or v is None)
                for k, v in condition.items()
            )
        
        deleted = 0
        
        for i in range(len(self) - 1, -1, -1):
            if predicate(self[i]):
                del self[i]
                deleted += 1
                if limit != -1 and deleted >= limit:
                    break
        
        return deleted
    
    def __setitem__(self, # type: ignore[override]
        index: SupportsIndex | slice, 
        value: ObjectType | list[ObjectType]):
        """Validate when setting an item by index."""
        if self._live_editor_mode:
            raise RuntimeError("Direct object editing is not supported in live editor mode yet")
        if isinstance(index, slice):
            if not isinstance(value, list):
                raise TypeError(f"can only assign a list (not {type(value).__name__}) to a slice")
            validated = [Object.wrap_object(obj) for obj in value]
            super().__setitem__(index, validated)
        else:
            if not isinstance(value, dict):
                raise TypeError(f"can only assign ObjectType dict (not {type(value).__name__})")
            validated = Object.wrap_object(value)
            super().__setitem__(index, validated)
    
    def append(self, obj: ObjectType):
        """Validate and append an object."""
        obj = Object.wrap_object(obj)
        if not self._live_editor_mode:
            super().append(obj)
        self.added_objects.append(obj)
    
    def insert(self, index: SupportsIndex, obj: ObjectType):
        """Validate and insert an object at index."""
        if self._live_editor_mode:
            raise RuntimeError("Direct item editing is not allowed in live editor mode yet")
        wrapped = Object.wrap_object(obj)
        super().insert(index, wrapped)
        self.added_objects.append(wrapped)
    
    def _append_without_tracking(self, obj: ObjectType):
        """For internal use only."""
        super().append(Object.wrap_object(obj))
    
    def extend(self, iterable: Iterable[ObjectType]):
        """Validate and extend with multiple objects."""
        validated = [Object.wrap_object(obj) for obj in iterable]
        if not self._live_editor_mode:
            super().extend(validated)
        self.added_objects.extend(validated)
    
    def __add__(self, other: object) -> "ObjectList":
        """Disabled: use extend() instead."""
        raise NotImplementedError("Use .extend() instead of + operator")
    
    def __iadd__(self, other: object) -> "ObjectList": 
        """Disabled: use extend() instead."""
        raise NotImplementedError("Use .extend() instead of += operator")


def _time_since_last(_state:list[float]=[time.perf_counter()]) -> float:
    now = time.perf_counter()
    a = _state[0]
    _state[0] = now
    return now - a


class Level:
    """Manages level state, loading, and exporting. Use from_file() or from_live_editor() to create an instance."""

    def __init__(self, *, live_editor: bool = False, tag_group: int = 9999):
        self.objects = ObjectList(live_editor=live_editor)
        """List of level's objects."""

        self.tag_group = tag_group
        """Deletes all objects with this group and adds this group to new added objects"""

        self._kit_level: KitLevel | None = None
        self._source_file: Path | None = None
        self._live_editor: LiveEditor | None = None

        self.new = IDAllocator(self.objects)

    @classmethod
    def from_file(cls, file_path: str | Path, tag_group: int = 9999) -> "Level":
        """Load a new Level from a .gmd file."""
        level = cls(live_editor=False, tag_group=tag_group)
        level._load_from_file(file_path)
        return level

    @classmethod
    def from_live_editor(cls, url: str = WEBSOCKET_URL, tag_group: int = 9999) -> "Level":
        """Load a new Level from the live editor."""
        level = cls(live_editor=True, tag_group=tag_group)
        level._load_from_live_editor(url)
        return level

    def _load_objects(self, kit_objects: KitObjectList, filename: str | None = None) -> None:
        """Load objects from gmdkit ObjectList into the objects list."""
        obj_count = len(kit_objects)

        for kit_obj in kit_objects:
            obj = from_kit_object(kit_obj)
            if self.tag_group not in obj.get(obj_prop.GROUPS, set()):
                self.objects._append_without_tracking(obj)

        print(f"\nLoaded {obj_count} objects from {filename or 'live editor'} in {_time_since_last():.3f} seconds.")
        print(f"\nRemoved {obj_count-len(self.objects)} objects with tag group {self.tag_group}, level is now {len(self.objects)} objects.")

    def _load_from_file(self, file_path: str | Path) -> None:
        """Internal: populate state from a .gmd file."""
        _time_since_last()

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Level file not found: {file_path=}")

        self.objects = ObjectList(live_editor=False)
        self.new = IDAllocator(self.objects)
        self._kit_level = KitLevel.from_file(path)
        self._source_file = path

        self._load_objects(self._kit_level.objects, filename=str(path))

    def _load_from_live_editor(self, url: str = WEBSOCKET_URL) -> None:
        """Internal: populate state from the live editor."""
        _time_since_last()

        self.objects = ObjectList(live_editor=True)
        self.new = IDAllocator(self.objects)
        self._live_editor = LiveEditor(url)
        self._live_editor.connect()
        self._live_editor.remove_objects(self.tag_group)
        _, kit_objects = self._live_editor.get_level()

        self._load_objects(kit_objects)

    def _validate_and_prepare_objects(self, validated_objects: ObjectList) -> None:
        """Run validation and preparation checks on objects before export."""

        targeted, used = get_trigger_targets(validated_objects)
        validate_target_exists(targeted, used)

        for obj in validated_objects.added_objects:
            groups = obj.get(obj_prop.GROUPS, {self.tag_group})
            groups.add(self.tag_group)
            obj[obj_prop.GROUPS] = groups

    def export_to_file(self, file_path: str | Path | None = None) -> None:
        """Export level to .gmd file."""

        print(f"\ngmdbuilder took {_time_since_last():.4f} seconds to prepare for export.")

        if self._kit_level is None:
            raise RuntimeError("No level loaded. Use Level.from_file() first")

        # Determine export path
        if file_path is None:
            if self._source_file is None:
                raise RuntimeError("No export path available. Provide file_path argument")

            if input("Overwrite the source file? [y,N]").lower() != 'y':
                raise RuntimeError("Export cancelled by user")
            export_path = self._source_file
        else:
            export_path = Path(file_path)

        self._validate_and_prepare_objects(self.objects)

        kit_objects = self._kit_level.objects
        kit_objects.clear()
        kit_objects.extend(to_kit_object(obj) for obj in self.objects)

        self._kit_level.to_file(str(export_path))

        print(f"\nExported level to {export_path} with {len(self.objects)} objects in {_time_since_last():.3f} seconds.\n")

    def export_to_live_editor(self, *, batch_size: int = 500) -> None:
        """Export level to live editor."""

        if self._live_editor is None:
            raise RuntimeError("No live editor connection. Use Level.from_live_editor() first")

        self._validate_and_prepare_objects(self.objects)

        # Convert to gmdkit ObjectList
        kit_objects = KitObjectList()
        kit_objects.extend(to_kit_object(obj) for obj in self.objects.added_objects)

        self._live_editor.add_objects(kit_objects, batch_size)
        self._live_editor.close()
        self._live_editor = None

        print(f"\nExported to live editor with {len(self.objects)} objects in {_time_since_last():.3f} seconds.\n")


IDTypes = Literal["group", "item", "color", "collision", "control"]

class IDAllocator:
    """Singleton class to manage unique ID allocation. Instance is 'new'."""
    
    def __init__(self, objects: list[ObjectType]):
        self._initialized = False
        self._object_list = objects
        
        self.used_group_ids: set[int] = set()
        self.used_item_ids: set[int] = set()
        self.used_color_ids: set[int] = set()
        self.used_collision_ids: set[int] = set()
        self.used_control_ids: set[int] = set()
        
        self._group_counter: int = 0
        self._item_counter: int = 0
        self._color_counter: int = 0
        self._collision_counter: int = 0
        self._control_counter: int = 0
        
        # Track the next candidate to check for each type (frontier optimization)
        self._group_frontier: int = 1
        self._item_frontier: int = 1
        self._color_frontier: int = 1
        self._collision_frontier: int = 1
        self._control_frontier: int = 1
    
    def reserve_id(self, id_type: IDTypes, id_values: int|tuple[int,...]):
        """Manually reserve IDs to exclude them from allocation."""
        
        ids = {id_values} if isinstance(id_values, int) else set(id_values)
        
        if id_type == "group":
            self.used_group_ids.update(ids)
        elif id_type == "item":
            self.used_item_ids.update(ids)
        elif id_type == "color":
            self.used_color_ids.update(ids)
        elif id_type == "collision":
            self.used_collision_ids.update(ids)
        elif id_type == "control":
            self.used_control_ids.update(ids)
        else:
            raise ValueError(f"Unknown ID type: {id_type}")
    
    def _register_free_ids(self):
        """Runs automatically at first new ID call."""
        self._initialized = True
        
        if len(self._object_list) == 0:
            raise RuntimeError("Objects not found. Load a level first with from_file() or from_live_editor()")
        
        for obj in self._object_list:
            id = obj[obj_prop.ID]
            if (key := obj_prop.GROUPS) in obj:
                self.used_group_ids.update(obj[key])

            if (key := obj_prop.COLOR_1) in obj:
                self.used_color_ids.add(obj[key])
            if (key := obj_prop.COLOR_2) in obj:
                self.used_color_ids.add(obj[key])
            if (key := obj_prop.Trigger.Color.COPY_ID) in obj:
                self.used_color_ids.add(obj[key])
            
            if id in (
                obj_id.Trigger.PICKUP, obj_id.Trigger.COUNT, obj_id.Trigger.INSTANT_COUNT
            ):
                if (key := obj_prop.Trigger.Count.ITEM_ID) in obj:
                    self.used_item_ids.add(obj[key])
            
            if id in (
                obj_id.Trigger.COLLISION, obj_id.Trigger.COLLISION_BLOCK
            ):
                if (key := obj_prop.Trigger.Collision.BLOCK_A) in obj:
                    self.used_collision_ids.add(obj[key])
                if (key := obj_prop.Trigger.Collision.BLOCK_B) in obj:
                    self.used_collision_ids.add(obj[key])
            
    
    def _get_next(self, pool_name: IDTypes) -> IntEnum:
        """Get next free ID by scanning forward from frontier. O(k) where k = skipped reserved IDs."""
        if not self._initialized:
            self._register_free_ids()
        
        used_set: set[int] = getattr(self, f"used_{pool_name}_ids")
        frontier: int = getattr(self, f"_{pool_name}_frontier")
        
        # Scan forward from frontier to find the next ID not already in use
        candidate = frontier
        while candidate <= 9999:
            if candidate not in used_set:
                break
            candidate += 1
        else:
            raise RuntimeError(f"No free {pool_name} IDs available (1-9999 range exhausted)")
        
        used_set.add(candidate)
        # Update frontier to next candidate for next call
        setattr(self, f"_{pool_name}_frontier", candidate + 1)
        
        counter: int = getattr(self, f"_{pool_name}_counter") + 1
        setattr(self, f"_{pool_name}_counter", counter)
        
        enum_cls = IntEnum(f"new_{pool_name}_{counter}", {f"ID_{candidate}": candidate})
        return enum_cls[f"ID_{candidate}"]  # type: ignore[return-value]
    
    
    @overload
    def group(self) -> IntEnum: ...
    @overload
    def group(self, count: Literal[1]) -> IntEnum: ... # type: ignore[override]
    @overload
    def group(self, count: Literal[2]) -> tuple[IntEnum, IntEnum]: ...
    @overload
    def group(self, count: int) -> tuple[IntEnum, ...]: ...
    def group(self, count: int = 1) -> tuple[IntEnum,...] | IntEnum:
        """Get next free group ID (1-9999)."""
        if count == 1:
            return self._get_next("group")
        return tuple(self._get_next("group") for _ in range(count))
    
    @overload
    def item(self) -> IntEnum: ...
    @overload
    def item(self, count: Literal[1]) -> IntEnum: ... # type: ignore[override]
    @overload
    def item(self, count: Literal[2]) -> tuple[IntEnum, IntEnum]: ...
    @overload
    def item(self, count: int) -> tuple[IntEnum, ...]: ...
    def item(self, count: int = 1) -> tuple[IntEnum,...] | IntEnum:
        """Get next free item ID (1-9999)."""
        if count == 1:
            return self._get_next("item")
        return tuple(self._get_next("item") for _ in range(count))
    
    @overload
    def color(self) -> IntEnum: ...
    @overload
    def color(self, count: Literal[1]) -> IntEnum: ... # type: ignore[override]
    @overload
    def color(self, count: Literal[2]) -> tuple[IntEnum, IntEnum]: ...
    @overload
    def color(self, count: int) -> tuple[IntEnum, ...]: ...
    def color(self, count: int = 1) -> tuple[IntEnum,...] | IntEnum:
        """Get next free color ID (1-9999)."""
        if count == 1:
            return self._get_next("color")
        return tuple(self._get_next("color") for _ in range(count))
    
    
    @overload
    def collision(self) -> IntEnum: ...
    @overload
    def collision(self, count: Literal[1]) -> IntEnum: ... # type: ignore[override]
    @overload
    def collision(self, count: Literal[2]) -> tuple[IntEnum, IntEnum]: ...
    @overload
    def collision(self, count: int) -> tuple[IntEnum, ...]: ...
    def collision(self, count: int = 1) -> tuple[IntEnum,...] | IntEnum:
        """Get next free collision block ID (1-9999)."""
        if count == 1:
            return self._get_next("collision")
        return tuple(self._get_next("collision") for _ in range(count))

