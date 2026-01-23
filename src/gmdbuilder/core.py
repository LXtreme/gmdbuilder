"""Core utilities for working with ObjectType dicts."""


from gmdbuilder.object_types import MoveType, ObjectType


def new_object(object_id: int) -> MoveType:
    return {
        'a1': 5
    }