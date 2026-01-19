
from gmdbuilder.object import Object
from gmdkit.mappings import obj_prop

ppt_od = obj_prop.trigger.on_death.ACTIVATE_GROUP
obj_prop.particle.DATA
class Level:
    file_path: str | None
    live_editor: bool = False
    queued_objects: list[Object] = []
    
    @classmethod
    def export_to(cls, *, file_path: str | None, live_editor: bool | None) -> None:
        if file_path is not None:
            cls.file_path = file_path
        if live_editor is not None:
            cls.live_editor = live_editor
    
    
    def queue_object(self, obj: Object):
        self.queued_objects.append(obj)
    
    
    def export_level(self) -> None:
        
        ...

