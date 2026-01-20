"""
Simple example showing how to use GMDBuilder's type-safe API.

This demonstrates the clean user-facing API without any gmdkit knowledge.
"""

from src.gmdbuilder.object import Object
from src.gmdbuilder.level import Level
from src.gmdbuilder.internal_mappings.obj_prop import ObjProp
from src.gmdbuilder.internal_mappings.obj_id import ObjId

# Create a new level
level = Level()

# Add a block
block = Object(1)
block[ObjProp.X] = 100
block[ObjProp.Y] = 100
block[ObjProp.COLOR_1] = 5
level.add_object(block)

# Add a spike
spike = Object(2)
spike[ObjProp.X] = 150
spike[ObjProp.Y] = 100
level.add_object(spike)

# Add a move trigger
move = Object(ObjId.Trigger.MOVE)
move[ObjProp.X] = 200
move[ObjProp.Y] = 100
move[ObjProp.Trigger.Move.TARGET_GROUP] = 1
move[ObjProp.Trigger.Move.MOVE_X] = 50
move[ObjProp.Trigger.Move.DURATION] = 1.0
level.add_object(move)

# Save the level
level.save("example_level.gmd")
print(f"Saved level with {level.object_count} objects")

# Load and modify
loaded = Level.from_file("example_level.gmd")
print(f"Loaded level with {len(loaded)} objects")

# Filter objects
blocks = loaded.filter_objects(lambda obj: obj.properties.get("a1") == ObjId.BLOCK)
print(f"Found {len(blocks)} blocks")

# Move all objects up by 50 units
for obj in loade