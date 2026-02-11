
from gmdkit.mappings import obj_prop
from gmdkit.models.level import Level
from gmdkit.models.object import Object

# open file
level = Level.from_file("example.gmd")

# get inner level properties
start = level.start

# get level objects as an ObjectList()
# object lists subclass list() so they can use all list methods alongside the ones defined by ListClass
# level.objects WILL throw AttributeError() if the level lacks an object string,
# or if you passed load = False to Level.from_file(), which skips loading objects
# LevelSave by default does not load the objects of levels
# so for any level you want to edit the objects of you must call level.load() first

obj_list = level.objects

print(f"obj_list has {len(obj_list)} objects.")

# filter by condition
after_origin = obj_list.where(lambda obj: obj.get(obj_prop.X, 0) > 0)
print(f" {len(after_origin)} objects have X > 0.")
# apply functions, kwargs are filtered for each called function
# ex: obj_func.fix_lighter has 'replacement' as a key argument
# after_origin.apply(obj_func.clean_duplicate_groups, obj_func.fix_lighter, replacement=0)

# create new object
new_obj = Object.default(1)
# set properties of object
# objects subclass dict() so they can use all dict methods alongside the ones defined by DictClass
new_obj.update(
  {
    obj_prop.X: 100,
    obj_prop.Y: 200,
    obj_prop.SCALE_X: 2,
    obj_prop.SCALE_Y: 2
  }
)

# append object to the level's object list
# can also be done directly to level.objects or level['k4'].objects (which level.objects references)
# lvl_prop.level.OBJECT_STRING also maps to 'k4'
obj_list.append(new_obj)

print(f"obj_list has {len(level.objects)} objects after adding new_obj.")
print(new_obj)

# export level
level.to_file("example_updated.gmd")
