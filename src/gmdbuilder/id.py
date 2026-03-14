

from enum import IntEnum
from typing import Iterable, Literal, overload
from .mappings import obj_id, obj_prop
from .object_types import ObjectType


IDTypes = Literal["group", "item", "color", "collision"]

class IDAllocator:
    """Class to manage unique ID allocation. Instance is 'new'."""
    
    def __init__(self, objects: list[ObjectType]):
        self._initialized = False
        
        self.used_group_ids: set[int] = set()
        self.used_item_ids: set[int] = set()
        self.used_color_ids: set[int] = set()
        self.used_collision_ids: set[int] = set()
        
        self._group_counter: int = 0
        self._item_counter: int = 0
        self._color_counter: int = 0
        self._collision_counter: int = 0
        
        self._group_frontier: int = 1
        self._item_frontier: int = 1
        self._color_frontier: int = 1
        self._collision_frontier: int = 1
    
    def reserve_id(self, id_type: IDTypes, id_values: int|Iterable[int]):
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
        else:
            raise ValueError(f"Unknown ID type: {id_type}")
    
    def register_free_ids_for_level(self, object_list: list[ObjectType]) -> None:
        """Runs automatically at level load."""
        if self._initialized:
            raise RuntimeError("IDAllocator is already initialized. register_free_ids_for_level() should only be called once at level load.")
        self._initialized = True
        
        if len(object_list) == 0:
            raise RuntimeError("Objects not found. Load a level first with from_file() or from_live_editor()")
        
        for obj in object_list:
            id = obj[obj_prop.ID]
            tid = obj_id.Trigger
            
            if (key := obj_prop.COLOR_1) in obj:
                self.used_color_ids.add(obj[key])
            if (key := obj_prop.COLOR_2) in obj:
                self.used_color_ids.add(obj[key])
            if (key := obj_prop.Trigger.Color.COPY_ID) in obj:
                self.used_color_ids.add(obj[key])
            
            if (key := obj_prop.GROUPS) in obj:
                self.used_group_ids.update(obj[key])
            
            if id in (tid.PICKUP, tid.COUNT, tid.INSTANT_COUNT):
                if (key := obj_prop.Trigger.Count.ITEM_ID) in obj:
                    self.used_item_ids.add(obj[key])
            
            if id in (tid.COLLISION, tid.COLLISION_BLOCK):
                if (key := obj_prop.Trigger.Collision.BLOCK_A) in obj:
                    self.used_collision_ids.add(obj[key])
                if (key := obj_prop.Trigger.Collision.BLOCK_B) in obj:
                    self.used_collision_ids.add(obj[key])
    
    def _get_next(self, pool_name: IDTypes) -> IntEnum:
        """Get next free ID by scanning forward from frontier. O(k) where k = skipped reserved IDs."""
        
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
    def group(self, count: Literal[3]) -> tuple[IntEnum, IntEnum, IntEnum]: ...
    @overload
    def group(self, count: Literal[4]) -> tuple[IntEnum, IntEnum, IntEnum, IntEnum]: ...
    @overload
    def group(self, count: Literal[5]) -> tuple[IntEnum, IntEnum, IntEnum, IntEnum, IntEnum]: ...
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
    def item(self, count: Literal[3]) -> tuple[IntEnum, IntEnum, IntEnum]: ...
    @overload
    def item(self, count: Literal[4]) -> tuple[IntEnum, IntEnum, IntEnum, IntEnum]: ...
    @overload
    def item(self, count: Literal[5]) -> tuple[IntEnum, IntEnum, IntEnum, IntEnum, IntEnum]: ...
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
    def color(self, count: Literal[3]) -> tuple[IntEnum, IntEnum, IntEnum]: ...
    @overload
    def color(self, count: Literal[4]) -> tuple[IntEnum, IntEnum, IntEnum, IntEnum]: ...
    @overload
    def color(self, count: Literal[5]) -> tuple[IntEnum, IntEnum, IntEnum, IntEnum, IntEnum]: ...
    @overload
    def color(self, count: int) -> tuple[IntEnum, ...]: ...
    def color(self, count: int = 1) -> tuple[IntEnum,...] | IntEnum:
        """Get next free color channel ID (1-9999)."""
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
    def collision(self, count: Literal[3]) -> tuple[IntEnum, IntEnum, IntEnum]: ...
    @overload
    def collision(self, count: Literal[4]) -> tuple[IntEnum, IntEnum, IntEnum, IntEnum]: ...
    @overload
    def collision(self, count: Literal[5]) -> tuple[IntEnum, IntEnum, IntEnum, IntEnum, IntEnum]: ...
    @overload
    def collision(self, count: int) -> tuple[IntEnum, ...]: ...
    def collision(self, count: int = 1) -> tuple[IntEnum,...] | IntEnum:
        """Get next free collision block ID (1-9999)."""
        if count == 1:
            return self._get_next("collision")
        return tuple(self._get_next("collision") for _ in range(count))

