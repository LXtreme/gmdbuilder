
# =================
# with .gmd file:
# =================

from gmdkit.models.level import Level
from gmdkit.models.object import Object, ObjectList
from gmdkit.mappings import obj_prop, obj_id

# READ - Load level from file
level = Level.from_file("example.gmd", load=True)
objects = level.objects  # ObjectList of Object (dict[int, Any])

# Work with int-dict form
for obj in objects:
    print(obj)  # {1: 1, 2: 50, 3: 45, ...}
    print(obj[2])  # Access X position via integer key
    print(obj.get(obj_prop.X))  # Or use mapping constant

# CREATE - Add new objects
new_obj = Object.default(1)  # Creates object with ID 1 (block)
new_obj[2] = 100  # X position
new_obj[3] = 200  # Y position
new_obj[obj_prop.GROUPS] = [1, 2, 3]  # Add to groups (auto-converts to IDList)

# Add to level
objects.append(new_obj)

# Or create from scratch
custom_obj = Object({
    1: 1,      # ID
    2: 300,    # X
    3: 400,    # Y
    57: [5]    # Groups (property 57 = GROUPS)
})
objects.append(custom_obj)

# UPDATE - Modify existing objects
for obj in objects:
    if obj.get(obj_prop.ID) == 1:  # Find all blocks (ID=1)
        obj[obj_prop.X] = obj.get(obj_prop.X, 0) + 50  # Move right by 50
        obj[obj_prop.SCALE_X] = 2  # Scale 2x

# Or update specific object
if len(objects) > 0:
    first_obj = objects[0]
    first_obj.update({
        obj_prop.X: 500,
        obj_prop.Y: 500,
        obj_prop.ROTATION: 45
    })

# DELETE - Remove objects by condition
# Method 1: Filter and reassign
objects_to_keep = [obj for obj in objects if obj.get(obj_prop.X, 0) <= 1000]
level.objects[:] = objects_to_keep  # Replace list contents

# Method 2: Use ObjectList.exclude() to remove and get removed items
removed = objects.exclude(lambda obj: obj.get(obj_prop.ID) == obj_id.trigger.MOVE)
print(f"Removed {len(removed)} move triggers")

# Method 3: Remove by index
if len(objects) > 0:
    objects.pop(0)  # Remove first object

# Method 4: Use where() to filter what you want to keep
blocks_only = objects.where(lambda obj: obj.get(obj_prop.ID) == 1)

# WRITE - Save back to file
level.to_file("example_modified.gmd")  # Saves to new file
# level.to_file("example.gmd")  # Or overwrite original

# BONUS: Working with object strings directly
raw_string = "1,1,2,50,3,45;"
obj_from_string = Object.from_string(raw_string)
print(obj_from_string)  # {1: 1, 2: 50.0, 3: 45.0}

# Convert back to string
string_out = obj_from_string.to_string()
print(string_out)  # "1,1,2,50,3,45;"

