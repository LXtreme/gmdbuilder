
from gmdbuilder.object import Object
from gmdkit.mappings import obj_prop
from gmdkit.models.level import Level as KitLevel

ppt_od = obj_prop.trigger.on_death.ACTIVATE_GROUP
obj_prop.particle.DATA
class Level:
    output_file_path: str | None
    output_live_editor: bool = False
    output_save_file: bool = False
    queued_objects: list[Object] = []
    gmdkit_level: KitLevel
    
    @classmethod
    def export_to(cls, *, 
        file_path: str | None, live_editor: bool | None, savefile: bool | None = None):
        """Choose save method"""
        if file_path is not None:
            cls.output_file_path = file_path
        elif live_editor is not None:
            cls.output_live_editor = live_editor
        elif savefile is not None:
            cls.output_save_file = savefile
    
    @classmethod
    def get_objects(cls) -> list[Object]:
        if cls.gmdkit_level is None:
            raise RuntimeError("No level loaded. Load with 'Level.from_file', 'Level.from_level' or 'Level.from_live_editor' first")
        return cls.gmdkit_level.objects
    
    @classmethod
    def add_object(cls, obj: Object):
        """Add object to queue"""
        cls.queued_objects.append(obj)
    
    @classmethod
    def export_level(cls):
        methods = { cls.output_file_path, cls.output_live_editor, cls.output_save_file }
        
        if sum(methods) != 1:
            raise RuntimeError("Choose only one output method, by calling 'Level.export_to' before export")
        
        cls.queued_objects.clear() # reset queue


    @classmethod
    def from_file(cls, file_path: str):
        """Load level from .gmd file"""

        return cls
    
    @classmethod
    def from_level(cls, level: str):
        """Load level from GD savefile"""
        
        return cls
    
    @classmethod
    def from_live_editor(cls):
        """Load level from WSLiveEditor"""
        return cls