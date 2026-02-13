"""
Simple example showing how to use GMDBuilder's type-safe API.

This demonstrates the clean user-facing API without any gmdkit knowledge.
"""

from gmdbuilder.object_types import CountType, MoveType
from gmdbuilder.mappings import obj_prop
from gmdbuilder.mappings import obj_id

from gmdbuilder import level
from gmdbuilder.validation import setting
from gmdbuilder.core import from_object_string, new_object


# 2 methods to load the level:
level.tag_group = 9999 # default is 9999 anyway
level.from_file("example.gmd")
# level.from_live_editor()

# set default tag group for new objects
# new objects get the group at export. to disable that feature, set tag_group to None.

# globally sets all validations to True. users will prob barely touch these ever so its a project global
setting.export.spawn_limit_check = False # disable check

all_objects = level.objects # can be mutated any way, but changes are intercepted and validated first

for obj in all_objects:
    if obj[obj_prop.ID] == obj_id.Trigger.MOVE:
        level.objects.remove(obj)

# block = from_raw_object({1: 1}) # required for putting into level.object and related methods

# all_objects.delete_where(block, limit=4) # deletes 4 match of block
# all_objects.delete_where(lambda obj: obj.get(ObjProp.ID) == 1) # deletes all matches of block

# load from level string
obj = from_object_string("1,1611,2,50,3,45;", obj_type=CountType) # translates to { a1:1611, a2:50, a3:45 }
obj[obj_prop.X] = 0
obj[obj_prop.Y] = 0
obj[obj_prop.GROUPS] = { 67 }
obj[obj_prop.Trigger.Count.ACTIVATE_GROUP] = True
# Add a block
movetrig: MoveType = new_object(901) # 'a<int>' dicts, returns ObjectType. new_object returns default props of obj_id 1
movetrig[obj_prop.X] = 100
movetrig[obj_prop.Trigger.Move.DURATION] = 5
movetrig[obj_prop.Trigger.Move.EASING] = 1
movetrig[obj_prop.Trigger.Move.TARGET_ID] = 68
all_objects.extend([movetrig, obj]) # validates on two stages; immediate and at export.

# g1, g2, g3 = level.new.group_multi(3)


# Choose 
level.export_to_file(file_path="example_updated.gmd") # adds all objects from level.objects. If not given and in file mode, ask to overwrite the file taken from the 'from_file' call
# level.export_to_live_editor() # for live_editor, adds all object in queue and clears queue.

