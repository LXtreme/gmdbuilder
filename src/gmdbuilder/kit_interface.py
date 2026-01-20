"""
This is all an AI generated attempt at making a type safe interface for most Gmdkit stuff.

I will be going back to this and fixing soon
"""

from typing import Any, TypeAlias
from pathlib import Path

# gmdkit imports - all the chaos lives in these imports
from gmdkit.models.level import Level as KitLevel  # type: ignore
from gmdkit.models.object import Object as KitObject, ObjectList as KitObjectList  # type: ignore
from gmdkit.defaults.objects import OBJECT_DEFAULT  # type: ignore

# Type aliases for clarity
KitLevelType: TypeAlias = Any  # The actual gmdkit Level type
KitObjectType: TypeAlias = Any  # The actual gmdkit Object type
KitObjectListType: TypeAlias = Any  # The actual gmdkit ObjectList type

# Raw object dict - uses integer keys (1, 2, 3, etc.) not the TypedDict string keys
RawObjectDict: TypeAlias = dict[int, Any]


class KitInterface:
    """
    Type-safe interface to gmdkit.
    
    All interactions with gmdkit go through this class.
    This isolates type unsafety to one place.
    """
    
    # ======================================================================
    # LEVEL LOADING
    # ======================================================================
    
    @staticmethod
    def load_level_from_file(file_path: str | Path) -> KitLevelType:
        """
        Load a level from a .gmd file.
        
        Args:
            file_path: Path to the .gmd file
            
        Returns:
            Loaded gmdkit Level object
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is invalid
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Level file not found: {file_path}")
        
        # gmdkit call - load=True ensures objects are loaded
        level = KitLevel.from_file(str(path), load=True)  # type: ignore
        
        # Verify objects loaded successfully
        if not hasattr(level, 'objects'):
            raise ValueError(f"Failed to load objects from level: {file_path}")
        
        return level
    
    @staticmethod
    def load_level_from_savefile(level_name: str) -> KitLevelType:
        """
        Load a level from GD save file.
        
        Args:
            level_name: Name of the level in the save file
            
        Returns:
            Loaded gmdkit Level object
            
        Note:
            This requires gmdkit to be able to locate the GD save file.
        """
        # TODO: Implement when save file support is needed
        raise NotImplementedError("Loading from save file not yet implemented")
    
    # ======================================================================
    # LEVEL SAVING
    # ======================================================================
    
    @staticmethod
    def save_level_to_file(level: KitLevelType, file_path: str | Path) -> None:
        """
        Save a level to a .gmd file.
        
        Args:
            level: The gmdkit Level object to save
            file_path: Where to save the level
        """
        path = Path(file_path)
        
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # gmdkit call - save=True ensures objects are saved
        level.to_file(str(path), save=True)  # type: ignore
    
    @staticmethod
    def save_level_to_savefile(level: KitLevelType, level_name: str) -> None:
        """
        Save a level to GD save file.
        
        Args:
            level: The gmdkit Level object to save
            level_name: Name to save the level as
        """
        # TODO: Implement when save file support is needed
        raise NotImplementedError("Saving to save file not yet implemented")
    
    # ======================================================================
    # OBJECT LIST OPERATIONS
    # ======================================================================
    
    @staticmethod
    def get_objects(level: KitLevelType) -> KitObjectListType:
        """
        Get the object list from a level.
        
        Args:
            level: The gmdkit Level object
            
        Returns:
            ObjectList containing all objects
            
        Raises:
            RuntimeError: If objects haven't been loaded
        """
        if not hasattr(level, 'objects'):
            raise RuntimeError(
                "Level objects not loaded. Load level with load=True or call level.load()"
            )
        
        return level.objects  # type: ignore
    
    @staticmethod
    def set_objects(level: KitLevelType, objects: KitObjectListType) -> None:
        """
        Replace the object list in a level.
        
        Args:
            level: The gmdkit Level object
            objects: New ObjectList to set
        """
        level.objects = objects  # type: ignore
    
    @staticmethod
    def create_empty_object_list() -> KitObjectListType:
        """
        Create an empty ObjectList.
        
        Returns:
            Empty gmdkit ObjectList
        """
        return KitObjectList()  # type: ignore
    
    # ======================================================================
    # OBJECT CREATION & MANIPULATION
    # ======================================================================
    
    @staticmethod
    def create_object_from_template(object_id: int) -> RawObjectDict:
        """
        Create an object dict from gmdkit's default template.
        
        Args:
            object_id: The GD object ID
            
        Returns:
            Dictionary with default properties for this object type
            
        Note:
            Returns a plain dict, not a gmdkit Object.
            Properties use integer keys (1, 2, 3, etc.)
        """
        # Get the default template from gmdkit
        template = OBJECT_DEFAULT.get(object_id, {})  # type: ignore
        
        # Ensure object_id (property 1) is set
        result: RawObjectDict = template.copy()  # type: ignore
        result[1] = object_id
        
        return result
    
    @staticmethod
    def create_kit_object_from_dict(obj_dict: RawObjectDict) -> KitObjectType:
        """
        Convert a dictionary to a gmdkit Object.
        
        Args:
            obj_dict: Dictionary with object properties
            
        Returns:
            gmdkit Object instance
        """
        obj = KitObject()  # type: ignore
        obj.update(obj_dict)  # type: ignore
        return obj
    
    @staticmethod
    def create_dict_from_kit_object(kit_obj: KitObjectType) -> RawObjectDict:
        """
        Convert a gmdkit Object to a dictionary.
        
        Args:
            kit_obj: gmdkit Object instance
            
        Returns:
            Dictionary with object properties
        """
        return dict(kit_obj)  # type: ignore
    
    @staticmethod
    def add_object_to_list(obj_list: KitObjectListType, obj_dict: RawObjectDict) -> None:
        """
        Add an object (as dict) to an ObjectList.
        
        Args:
            obj_list: The gmdkit ObjectList
            obj_dict: Object dictionary to add
        """
        kit_obj = KitInterface.create_kit_object_from_dict(obj_dict)
        obj_list.append(kit_obj)  # type: ignore
    
    @staticmethod
    def add_kit_object_to_list(obj_list: KitObjectListType, kit_obj: KitObjectType) -> None:
        """
        Add a gmdkit Object to an ObjectList.
        
        Args:
            obj_list: The gmdkit ObjectList
            kit_obj: gmdkit Object to add
        """
        obj_list.append(kit_obj)  # type: ignore
    
    # ======================================================================
    # OBJECT LIST QUERIES
    # ======================================================================
    
    @staticmethod
    def get_object_count(obj_list: KitObjectListType) -> int:
        """
        Get the number of objects in the list.
        
        Args:
            obj_list: The gmdkit ObjectList
            
        Returns:
            Number of objects
        """
        return len(obj_list)  # type: ignore
    
    @staticmethod
    def iter_objects(obj_list: KitObjectListType) -> list[RawObjectDict]:
        """
        Iterate over objects as dictionaries.
        
        Args:
            obj_list: The gmdkit ObjectList
            
        Returns:
            List of object dictionaries
        """
        return [dict(obj) for obj in obj_list]  # type: ignore
    
    @staticmethod
    def filter_objects_by_id(obj_list: KitObjectListType, object_id: int) -> list[RawObjectDict]:
        """
        Filter objects by their object ID (property 1).
        
        Args:
            obj_list: The gmdkit ObjectList
            object_id: The object ID to filter by
            
        Returns:
            List of matching object dictionaries
        """
        result: list[RawObjectDict] = []
        for obj in obj_list:  # type: ignore
            obj_dict: RawObjectDict = dict(obj)  # type: ignore
            if obj_dict.get(1) == object_id:  # Property 1 is object ID
                result.append(obj_dict)
        return result
    
    @staticmethod
    def filter_objects_by_group(obj_list: KitObjectListType, group_id: int) -> list[RawObjectDict]:
        """
        Filter objects that belong to a specific group.
        
        Args:
            obj_list: The gmdkit ObjectList
            group_id: The group ID to filter by
            
        Returns:
            List of matching object dictionaries
            
        Note:
            Property 57 contains groups (can be a single int or list)
        """
        result: list[RawObjectDict] = []
        for obj in obj_list:  # type: ignore
            obj_dict: RawObjectDict = dict(obj)  # type: ignore
            groups = obj_dict.get(57)  # Property 57 is groups
            
            # Handle both single int and list of ints
            if isinstance(groups, int) and groups == group_id:
                result.append(obj_dict)
            elif isinstance(groups, list) and group_id in groups:
                result.append(obj_dict)
        
        return result
    
    # ======================================================================
    # LEVEL PROPERTIES
    # ======================================================================
    
    @staticmethod
    def get_level_name(level: KitLevelType) -> str:
        """
        Get the level's name.
        
        Args:
            level: The gmdkit Level object
            
        Returns:
            Level name
        """
        # Level is a dict subclass, key 'k2' is the level name
        return level.get('k2', 'Unnamed')  # type: ignore
    
    @staticmethod
    def set_level_name(level: KitLevelType, name: str) -> None:
        """
        Set the level's name.
        
        Args:
            level: The gmdkit Level object
            name: New level name
        """
        level['k2'] = name  # type: ignore
    
    # ======================================================================
    # ENCODING/DECODING (for serialization)
    # ======================================================================
    
    @staticmethod
    def encode_object_to_string(obj_dict: RawObjectDict) -> str:
        """
        Encode an object dict to GD's string format.
        
        Args:
            obj_dict: Object dictionary
            
        Returns:
            Encoded string (comma-separated key,value pairs)
        """
        kit_obj = KitInterface.create_kit_object_from_dict(obj_dict)
        return kit_obj.to_string()  # type: ignore
    
    @staticmethod
    def decode_object_from_string(obj_string: str) -> RawObjectDict:
        """
        Decode a GD object string to a dict.
        
        Args:
            obj_string: Encoded object string
            
        Returns:
            Object dictionary
        """
        kit_obj = KitObject.from_string(obj_string)  # type: ignore
        return dict(kit_obj)  # type: ignore
    
    # ======================================================================
    # VALIDATION HELPERS
    # ======================================================================
    
    @staticmethod
    def is_valid_object_dict(obj_dict: RawObjectDict) -> bool:
        """
        Basic validation that an object dict is valid.
        
        Args:
            obj_dict: Object dictionary to validate
            
        Returns:
            True if valid, False otherwise
            
        Note:
            Just checks that required property 1 (object ID) exists.
            Does NOT do full validation - that's your job!
        """
        return 1 in obj_dict and isinstance(obj_dict[1], int)
    
    @staticmethod
    def get_object_id(obj_dict: RawObjectDict) -> int | None:
        """
        Get the object ID (property 1) from an object dict.
        
        Args:
            obj_dict: Object dictionary
            
        Returns:
            Object ID, or None if not present
        """
        return obj_dict.get(1)  # type: ignore
    
    @staticmethod
    def get_object_groups(obj_dict: RawObjectDict) -> list[int]:
        """
        Get all group IDs an object belongs to.
        
        Args:
            obj_dict: Object dictionary
            
        Returns:
            List of group IDs (empty if none)
        """
        groups = obj_dict.get(57)  # Property 57 is groups
        
        if groups is None:
            return []
        elif isinstance(groups, int):
            return [groups]
        elif isinstance(groups, list):
            return groups
        else:
            return []


# ======================================================================
# CONVENIENCE FUNCTIONS (optional, for cleaner imports)
# ======================================================================

def load_level(file_path: str | Path) -> KitLevelType:
    """Convenience wrapper for KitInterface.load_level_from_file"""
    return KitInterface.load_level_from_file(file_path)

def save_level(level: KitLevelType, file_path: str | Path) -> None:
    """Convenience wrapper for KitInterface.save_level_to_file"""
    KitInterface.save_level_to_file(level, file_path)

def get_objects(level: KitLevelType) -> KitObjectListType:
    """Convenience wrapper for KitInterface.get_objects"""
    return KitInterface.get_objects(level)

def create_object(object_id: int) -> RawObjectDict:
    """Convenience wrapper for KitInterface.create_object_from_template"""
    return KitInterface.create_object_from_template(object_id)