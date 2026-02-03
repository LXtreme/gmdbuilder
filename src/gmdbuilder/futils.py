"""Framework utilities. Not for users."""
from functools import lru_cache


@lru_cache(maxsize=4096)
def translate_group_string(group_string: str) -> set[int]:
    """Returns new group set from dot-seperated int list"""
    parts = group_string.split(".")
    s: set[int] = set()
    for group in parts:
        g = int(group)
        if g in s:
            raise ValueError(f"Group string contains duplicates:\n{group_string=}")
        s.add(g)
    
    return s


@lru_cache(maxsize=4096)
def translate_remap_string(remap_string: str) -> dict[int, int]:
    """Returns 'dict[source] = target' from dot-seperated int-string"""
    if not remap_string:
        raise ValueError("Remap string is empty")
    
    parts = remap_string.split(".")

    if len(parts) % 2 != 0:
        raise ValueError(
            f"Remap string must contain an even number of parts:\n{remap_string}")

    pairs: dict[int, int] = {}
    it = iter(parts)
    for source_str, target_str in zip(it, it):
        source = int(source_str)
        target = int(target_str)

        if source in pairs:
            raise ValueError(f"Duplicate source '{source}' in remap string:\n{remap_string}")
        if source == target:
            raise ValueError(f"Redundant mapping found in remap string:\n{remap_string=}")
        
        pairs[source] = target
        
    return pairs