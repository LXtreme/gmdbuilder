"""
Script to generate new_object overloads for core.pyi from fields.py

Reads ID_TO_TYPEDDICT and generates @overload stubs for each object ID.
Outputs to output.txt for manual insertion into core.pyi
"""

import sys
from pathlib import Path

from gmdbuilder.fields import ID_TO_TYPEDDICT

# Add src to path so we can import gmdbuilder modules
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

def get_typeddict_name(typeddict_type: type) -> str:
    """Extract the name of a TypedDict class."""
    return typeddict_type.__name__


def generate_overloads() -> str:
    """Generate all new_object overloads from ID_TO_TYPEDDICT."""
    lines: list[str] = []
    
    # Collect all unique (object_id, TypedDict) pairs and sort by ID
    id_type_pairs = sorted(ID_TO_TYPEDDICT.items(), key=lambda x: x[0])
    
    # Group by TypedDict type to avoid duplicate overloads for the same return type
    # (though we still want separate overloads for each ID)
    seen_pairs: set[tuple[int, str]] = set()
    
    for obj_id, typeddict_type in id_type_pairs:
        # Create a unique key for this overload
        pair_key = (obj_id, typeddict_type.__name__)
        
        if pair_key in seen_pairs:
            continue
        seen_pairs.add(pair_key)
        
        typeddict_name = get_typeddict_name(typeddict_type)
        lines.append("@overload")
        lines.append(f"def is_obj_id(obj: ObjectType, object_id: Literal[{obj_id}]) -> TypeGuard[td.{typeddict_name}]: ...")
    
    return "\n".join(lines)


# def is_obj_id(obj: ObjectType, object_id: Literal[4539]) -> TypeGuard[td.CollectibleType]: ...
def main():
    overloads = generate_overloads()
    
    output_path = Path(__file__).parent / "output.txt"
    
    with open(output_path, "w") as f:
        f.write(overloads)
    
    print(f"Generated {len(overloads.splitlines()) // 2} overloads")
    print(f"Output written to: {output_path}")


if __name__ == "__main__":
    main()