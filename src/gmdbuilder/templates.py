
class ObjProp(str):
    ID = "a1"
    X = "a2"
    Y = "a3"
    FLIP_X = "a4"
    FLIP_Y = "a5"
    ROTATION = "a6"
    class Trigger(str):
        TOUCH_TRIGGER = "a11"
        EDITOR_PREVIEW = "a13"
        INTERACTIBLE = "a36"
        SPAWN_TRIGGER = "a62"
        MULTI_TRIGGER = "a87"
        class Move(str):
            DURATION = "a10"
            MOVE_X = "a28"
            MOVE_Y = "a29"
            EASING = "a30"
            TARGET_ID = "a51"


class ObjectType(TypedDict, total=False):
    a1: int  # ID
    a2: float  # X
    a3: float  # Y
    a4: bool  # FLIP_X
    a5: bool  # FLIP_Y
    a6: float  # ROTATION

class TriggerType(ObjectType, total=False):
    a11: bool  # TOUCH_TRIGGER
    a13: bool  # EDITOR_PREVIEW
    a36: bool  # INTERACTIBLE
    a62: bool  # SPAWN_TRIGGER
    a87: bool  # MULTI_TRIGGER

class MoveType(TriggerType, total=False):
    a10: float  # DURATION
    a28: int  # MOVE_X
    a29: int  # MOVE_Y
    a30: Any  # EASING
    a51: Required[int]  # TARGET_ID