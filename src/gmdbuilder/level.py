"""Type-safe level interface for Geometry Dash."""

from pathlib import Path

from gmdkit.models.level import Level as KitLevel  # type: ignore
from gmdkit.models.object import ObjectList as KitObjectList, Object as KitObject  # type: ignore
from gmdkit.extra.live_editor import LiveEditor  # type: ignore

from gmdbuilder.object_types import ObjectType
from gmdbuilder.validation import ValidationError

WEBSOCKET_URL_DEFAULT = "ws://127.0.0.1:1313" # for live server default URl, same as gmdkit's default

objects: list[ObjectType] = []

def Object():
    """Create a new object that automatically gets queued."""

class Level:
    """
    Singleton level interface for Geometry Dash.
    
    Usage:
        Level.from_file("level.gmd")
        
        obj = Object(1)
        obj['a2'] = 100
        obj['a3'] = 200
        Level.objects.append(obj)
        
        Level.export("output.gmd")
    """
    
    _kit_level: KitLevel | None = None
    _export_path: str | Path | None = None
    _live_editor: LiveEditor | None = None
    _live_editor_connected: bool = False
    objects: list[ObjectType] = []
    object_queue: list[ObjectType] = []
    
    @classmethod
    def from_file(cls, file_path: str | Path):
        """Load level from .gmd file"""
        cls._kit_level = KitLevel.from_file(str(file_path))
        cls._load_objects_from_kit()
    
    @classmethod
    def from_live_editor(cls, url: str | None = None):
        """
        Load level from WSLiveEditor, iAndyHD3's Geode Mod.
        Github Link: https://github.com/iAndyHD3/WSLiveEditor
        """
        cls._live_editor = LiveEditor(url or WEBSOCKET_URL_DEFAULT)
        cls._live_editor.connect()
        cls._live_editor_connected = True
    
    @classmethod
    def _load_objects_from_kit(cls) -> None:
        """Internal: Load objects from kit level into typed dict format"""
        if cls._kit_level is None:
            raise RuntimeError("No level loaded")
        
        cls.objects = []
        for kit_obj in cls._kit_level.objects:
            # Convert int keys to 'a<int>' string keys
            typed_obj: ObjectType = {} # type: ignore
            for int_key, value in kit_obj.items():
                str_key = f"a{int_key}"
                typed_obj[str_key] = value
            cls.objects.append(typed_obj)
    
    @classmethod
    def export(cls, file_path: str | Path | None = None) -> None:
        """Export level to file or live editor.

        Args:
            file_path: Path to save to. Will override the source path if not given.
        """
        if cls._kit_level is None and not cls._live_editor_connected:
            raise RuntimeError("No level loaded. Use Level.from_file() or Level.from_live_editor() first")
        
        for obj in cls.object_queue:
            for resolve in obj.get('_pending_validations', []):
                try:
                    resolve(cls.objects, cls.object_queue)
                except ValidationError as e:
                    raise ValidationError(f"Validation failed for queued object: {e}")
            cls.objects.append(obj)
        cls.object_queue.clear()
        
        if file_path:
            cls._export_to_file(str(file_path))
        elif cls._live_editor_connected:
            cls._export_to_live_editor()
        else:
            raise RuntimeError("No export destination. Provide file_path or use Level.from_live_editor()")
    
    @classmethod
    def _export_to_file(cls, file_path: str) -> None:
        """Internal: Save to .gmd file"""
        if cls._kit_level is None:
            raise RuntimeError("Cannot export to file without loaded level")
        
        cls._sync_objects_to_kit()
        cls._kit_level.to_file(file_path)
    
    @classmethod
    def _export_to_live_editor(cls) -> None:
        """Internal: Send to WSLiveEditor"""
        if cls._live_editor is None:
            raise RuntimeError("Live editor not connected")
        
        # Convert typed dicts back to int keys and create kit objects
        kit_objects = KitObjectList()
        for obj in cls.objects:
            kit_obj_dict = {}
            for str_key, value in obj.items():
                if str_key.startswith('a') and len(str_key) > 1:
                    int_key = int(str_key[1:])
                    kit_obj_dict[int_key] = value
            
            kit_obj = KitObject()
            kit_obj.update(kit_obj_dict)
            kit_objects.append(kit_obj)
        
        cls._live_editor.add_objects(kit_objects)
    
    @classmethod
    def _sync_objects_to_kit(cls) -> None:
        """Internal: Sync typed dicts back to kit level"""
        if cls._kit_level is None:
            raise RuntimeError("No level loaded")
        
        kit_objects = KitObjectList()
        for obj in cls.objects:
            # Convert 'a<int>' keys back to int keys
            kit_obj_dict = {}
            for str_key, value in obj.items():
                if str_key.startswith('a') and len(str_key) > 1:
                    int_key = int(str_key[1:])
                    kit_obj_dict[int_key] = value
            
            kit_obj = KitObject()
            kit_obj.update(kit_obj_dict)
            kit_objects.append(kit_obj)
        
        cls._kit_level.objects = kit_objects
    
    # ===== Utilities =====
    
    @classmethod
    def disconnect_live_editor(cls) -> None:
        """Disconnect from WSLiveEditor"""
        if cls._live_editor:
            cls._live_editor.close()
        cls._live_editor = None
        cls._live_editor_connected = False
    