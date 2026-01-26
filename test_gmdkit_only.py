"""
Simple test to verify gmdkit save/load functionality works correctly.
This test will PASS when gmdkit is fixed to properly save and reload levels.

Expected behavior:
1. Load a level
2. Add an object
3. Save to file
4. Reload from file
5. Verify objects are present

Current status: FAILS due to gmdkit serialization bug with ObjectString type.
"""

import os
import sys

from gmdkit.mappings import obj_prop
from gmdkit.models.level import Level
from gmdkit.models.object import Object


def test_gmdkit_save_load():
    """Test that gmdkit can save and reload a modified level."""
    
    # 1. Load oiginal level
    level = Level.from_file("example.gmd")
    original_objects = level.objects
    original_count = len(original_objects)
    print(f"Loaded level with {original_count} objects")

    # 2. Add a new object
    new_obj = Object.default(1)  # Block
    new_obj[obj_prop.X] = 999
    new_obj[obj_prop.Y] = 999
    original_objects.append(new_obj)
    new_count = len(original_objects)
    print(f"Added object, now {new_count} objects")
    
    # 3. Save to file
    test_file = "test_gmdkit_roundtrip.gmd"
    level.save()  # Encode objects into level string
    level.to_file(test_file)
    print(f"Saved to {test_file}")
    
    # 4. Reload from file
    level2 = Level.from_file(test_file)
    
    # 5. Verify objects are present
    try:
        reloaded_objects = level2.objects
        reloaded_count = len(reloaded_objects)
        print(f"Reloaded {reloaded_count} objects")
        
        # Check count matches
        if reloaded_count == new_count:
            print("✅ PASS: Object count matches!")
            return True
        else:
            print(f"❌ FAIL: Expected {new_count} objects, got {reloaded_count}")
            return False
            
    except AttributeError as e:
        print(f"❌ FAIL: Could not access level2.objects - {e}")
        return False
    
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    success = test_gmdkit_save_load()
    sys.exit(0 if success else 1)