from .object import Object
from .trigger import Trigger

from .transform import Move, Rotate, Scale
from .color import Color, Pulse, Alpha, Toggle, Animate
from .control import Spawn, Count, Touch
from .follow import Follow, Shake

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
    "Count",
    "Touch",
    # follow.py
    "Follow",
    "Shake",
]
