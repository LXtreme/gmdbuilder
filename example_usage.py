"""
Simple example showing how to use GMDBuilder's type-safe API.

This demonstrates the clean user-facing API without any gmdkit knowledge.
"""

from gmdbuilder.object_typeddict import MoveType
from gmdbuilder.mappings.obj_prop import ObjProp
from gmdbuilder.mappings.obj_id import ObjId

from gmdbuilder import level
from gmdbuilder.validation import setting
from gmdbuilder.core import to_raw_object, from_object_string, new_object, from_raw_object


# 2 methods to load the level:
level.from_file("example.gmd")

# level.from_live_editor()
level.tag_group = 9999 # default is 9999 anyway
# new objects get the group at export. to disable that feature, set tag_group to None.

# globally sets all validations to True. users will prob barely touch these ever so its a project global
setting.export_spawn_limit_check = False # disable check

all_objects = level.objects # can be mutated any way, but changes are intercepted and validated first

for obj in all_objects:
    if obj[ObjProp.ID] == ObjId.Trigger.MOVE:
        print('debug mode to see raw move trigger:')
        print(to_raw_object(obj))
        # level.objects.delete(obj) # raise error if not exact match found

block = from_raw_object({1: 1}) # required for putting into level.object and related methods

all_objects.delete_where(block, limit=4) # deletes 4 match of block
all_objects.delete_where(lambda obj: obj.get(ObjProp.ID) == 1) # deletes all matches of block

# load from level string
obj = from_object_string("1,1,2,50,3,45;") # translates to { a1:1, a2:50, a3:45 }, is type ObjectType
obj[ObjProp.X] = 0
obj[ObjProp.Y] = 0
obj[ObjProp.GROUPS] = { -5 }
# Add a block
movetrig: MoveType = new_object(901) # 'a<int>' dicts, returns ObjectType. new_object returns default props of obj_id 1
movetrig[ObjProp.X] = 100
movetrig[ObjProp.Trigger.Move.DURATION] = 5
all_objects.extend([movetrig, obj]) # validates on two stages; immediate and at export.

g1, g2, g3 = level.new.group_multi(3)

# from gmdbuilder.template import TriggerTemplate

# def my_custom_move(time, target, distance):
#     level.objects.append(TriggerTemplate.move(x=0, y=0, 
#         target=target, time=time, distance=distance, easing=0, easing_rates=0))
# # or
# def my_custom_move2(time, target, distance):
#     return TriggerTemplate.move(x=0, y=0, 
#         target=target, time=time, distance=distance, easing=0, easing_rates=0)
# # or
# def my_custom_move3(time, target, distance):
#     with template.autoadd_mode():
#         TriggerTemplate.move(x=0, y=0, 
#             target=target, time=time, distance=distance, easing=0, easing_rates=0)

# my_custom_move(1.0, 12, 50)

# level.objects.append(my_custom_move2(1,4,30))

# Choose 
level.export_to_file(file_path="example_updated.gmd") # adds all objects from level.objects. If not given and in file mode, ask to overwrite the file taken from the 'from_file' call
# level.export_to_live_editor() # for live_editor, adds all object in queue and clears queue.

