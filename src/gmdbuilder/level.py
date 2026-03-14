"""Level loading and exporting for Geometry Dash."""

import time

from pathlib import Path

from .color import Color, KitColor
from gmdkit.extra.live_editor import WEBSOCKET_URL, LiveEditor
from gmdkit.models.level import Level as KitLevel
from gmdkit.models.object import ObjectList as KitObjectList, Object as KitObject
from gmdkit.models.prop.color import ColorList as KitColorList

from .core import from_kit_object, to_kit_object
from .id import IDAllocator
from .mappings import obj_prop
from .object import ObjectList


def _time_since_last(_state:list[float]=[time.perf_counter()]) -> float:
    now = time.perf_counter()
    a = _state[0]
    _state[0] = now
    return now - a


class Level:
    """Manages level state, loading, and exporting. Use from_file() or from_live_editor() to create an instance."""

    def __init__(self, *, live_editor: bool = False, tag_group: int = 9999):
        self.objects = ObjectList(tag_group=tag_group)
        """List of level's objects. Newly appended objects are stamped with tag_group."""

        self._kit_level: KitLevel | None = None
        self._source_file: Path | None = None
        self._live_editor: LiveEditor | None = None
        self._color_dict: dict[int, KitColor] = {}
        self._color_list = KitColorList()
        
        self.color: dict[int, Color] = {}
        """
        Mapping of Color channel ID to Color dataclass.
        Modifying these colors will update the level's colors on export.
        """

        self.new = IDAllocator(self.objects)
        """Get 'next free' group/item/color/collision IDs"""
    
    def _load_colors(self, start_object: KitObject) -> None:
        self._color_list = start_object[obj_prop.Level.COLORS]
        for c in self._color_list:
            self.color[c.channel] = Color.from_kit_color(c)
            self._color_dict[c.channel] = c
            self.new.used_color_ids.add(c.channel)
    
    def _export_colors(self) -> None:
        for channel, color in self.color.items():
            if channel in self._color_dict:
                color.map_to_kit_color(self._color_dict[channel])
            else:
                kit_col = color.to_kit_color(channel)
                self._color_dict[channel] = kit_col
                self._color_list.append(kit_col)
    
    def _load_objects(self, 
        kit_objects: KitObjectList, 
        obj_count: int, 
        filename: str | None = None
    ) -> None:
        tag_group = self.objects.tag_group

        for kit_obj in kit_objects:
            obj = from_kit_object(kit_obj)
            groups = obj.get(obj_prop.GROUPS, {})
            if tag_group not in groups:
                list.append(self.objects, obj) # type: ignore
        
        self.new.register_free_ids_for_level(self.objects)
        
        print(f"\nLoaded {obj_count} objects from {filename or 'WSLiveEditor'} " 
              f"in {_time_since_last():.3f} seconds."
              f"\n\nRemoved {obj_count-len(self.objects)} objects with "
              f"tag group {tag_group}, level is now {len(self.objects)} objects.")

    @classmethod
    def from_file(cls, file_path: str | Path, tag_group: int = 9999) -> "Level":
        """Load a new Level from a .gmd file."""
        level = cls(live_editor=False, tag_group=tag_group)
        
        _time_since_last()

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Level file not found: {file_path=}")
        
        level._kit_level = KitLevel.from_file(path)
        level._source_file = path
        
        level._load_colors(level._kit_level.start)
        
        obj_count = len(level._kit_level.objects)
        level._load_objects(level._kit_level.objects, obj_count, filename=str(path))
        return level

    @classmethod
    def from_live_editor(cls, url: str = WEBSOCKET_URL, tag_group: int = 9999) -> "Level":
        """Load a new Level from the live editor."""
        level = cls(live_editor=True, tag_group=tag_group)
        
        _time_since_last()
        
        level._live_editor = LiveEditor(url)
        level._live_editor.connect()
        start, objects = level._live_editor.get_level()
        obj_count = len(objects)
        
        level._live_editor.remove_objects(level.objects.tag_group)
        level._load_colors(start)

        level._load_objects(objects, obj_count)
        return level

    def export_to_file(self, file_path: str | Path | None = None):
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
        
        self._kit_level.objects.clear()
        self._kit_level.objects.extend(to_kit_object(obj) for obj in self.objects)
        self._export_colors()
        
        self._kit_level.to_file(str(export_path))
        
        print(f"\nExported level to {export_path} with {len(self.objects)} objects in {_time_since_last():.3f} seconds.\n")

    def export_to_live_editor(self):
        """Export level to live editor. Level must be open."""
        
        if self._live_editor is None:
            raise RuntimeError("No live editor connection. Use Level.from_live_editor() first")
        
        self._live_editor.objects.clear()
        self._live_editor.objects.extend(to_kit_object(obj) for obj in self.objects)
        self._export_colors()
        
        self._live_editor.replace_level(save_string=True)
        self._live_editor.close()
        self._live_editor = None
        
        print(f"\nExported to live editor with {len(self.objects)} objects in {_time_since_last():.3f} seconds.\n")

