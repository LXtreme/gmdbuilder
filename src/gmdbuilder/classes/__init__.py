from .object import Object
from .trigger import Trigger

from .transform import Move, Rotate, Scale
from .color import Color, Pulse, Alpha, Toggle, Animate
from .control import Spawn, Touch
from .item import Pickup, Count, InstantCount, ItemCompare, ItemEdit, ItemPersist
from .follow import Follow, Shake, FollowPlayerY, AdvFollow, EditAdvFollow

__all__ = [
    # Base
    "Object",
    "Trigger",
    # transform.py
    "Move",
    "Rotate",
    "Scale",
    # color.py
    "Color",
    "Pulse",
    "Alpha",
    "Toggle",
    "Animate",
    # control.py
    "Spawn",
    "Touch",
    # item.py
    "Pickup",
    "Count",
    "InstantCount",
    "ItemCompare",
    "ItemEdit",
    "ItemPersist",
    # follow.py
    "Follow",
    "Shake",
    "FollowPlayerY",
    "AdvFollow",
    "EditAdvFollow",
]
