from enum import IntEnum

class PlayerSpeed:
    SLOW = 0.7 * 5.98000200 * 60
    NORMAL = 0.9 * 5.77000189 * 60
    FAST = 1.1 * 5.87000200 * 60
    VERY_FAST = 1.3 * 5.77000189 * 60
    SUPER_FAST = 1.6 * 5.77000189 * 60


class Easing(IntEnum):
    NONE = 0
    EASE_IN_OUT = 1
    EASE_IN = 2
    EASE_OUT = 3
    ELASTIC_IN_OUT = 4
    ELASTIC_IN = 5
    ELASTIC_OUT = 6
    BOUNCE_IN_OUT = 7
    BOUNCE_IN = 8
    BOUNCE_OUT = 9
    EXPONENTIAL_IN_OUT = 10
    EXPONENTIAL_IN = 11
    EXPONENTIAL_OUT = 12
    SINE_IN_OUT = 13
    SINE_IN = 14
    SINE_OUT = 15
    BACK_IN_OUT = 16
    BACK_IN = 17
    BACK_OUT = 18

class ItemLabel(IntEnum):
    pass

    class Alignment(IntEnum):
        CENTER = 0
        LEFT = 1
        RIGHT = 2

    class SpecialId(IntEnum):
        MAINTIME = -1
        POINTS = -2
        ATTEMPTS = -3

class LevelPlayerColor17(IntEnum):
    NONE = 0
    PLAYER_1 = 1
    PLAYER_2 = 2

class OldColor(IntEnum):
    PLAYER_1 = 1
    PLAYER_2 = 2
    COLOR_1 = 3
    COLOR_2 = 4
    LIGHT_BG = 5
    COLOR_3 = 6
    COLOR_4 = 7
    LINE_3D = 8

class SingleColorType(IntEnum):
    DEFAULT = 0
    BASE = 1
    DETAIL = 2

class Trigger(IntEnum):
    pass

    class AdvFollow(IntEnum):
        pass

        class Init(IntEnum):
            INIT = 0
            SET = 1
            ADD = 2

        class Mode(IntEnum):
            MODE_1 = 0
            MODE_2 = 1
            MODE_3 = 2

    class ArrowDirection(IntEnum):
        NONE = 0
        UP = 1
        DOWN = 2
        LEFT = 3
        RIGHT = 4

    class BpmSpeed(IntEnum):
        NORMAL = 0
        SLOW = 1
        FAST = 2
        VERY_FAST = 3
        SUPER_FAST = 4

    class CameraEdgeDirection(IntEnum):
        NONE = 0
        LEFT = 1
        RIGHT = 2
        UP = 3
        DOWN = 4

    class Effect(IntEnum):
        pass

        class EnterOnly(IntEnum):
            NONE = 0
            ENTER = 1
            EXIT = 2

        class SpecialCenter(IntEnum):
            P1 = -1
            P2 = -2
            C = -3
            BL = -4
            CL = -5
            TL = -6
            BC = -7
            TC = -8
            BR = -9
            CR = -10
            TR = -11

    class EnterOnlyPreset(IntEnum):
        NONE = 0
        ENTER = 1
        EXIT = 2

    class Gradient(IntEnum):
        pass

        class Blending(IntEnum):
            NORMAL = 0
            ADDITIVE = 1
            MULTIPLY = 2
            INVERT = 3

        class Layer:
            BG = 1
            MG = 2
            B5 = 3
            B4 = 4
            B3 = 5
            B2 = 6
            B1 = 7
            P = 8
            T1 = 9
            T2 = 10
            T3 = 11
            T4 = 12
            G = 13
            UI = 14
            MAX = 15

    class InstantCountMode(IntEnum):
        EQUAL = 0
        LARGER = 1
        SMALLER = 2

    class Item(IntEnum):
        pass

        class MathOp(IntEnum):
            ADD = 1
            SUBTRACT = 2
            MULTIPLY = 3
            DIVIDE = 4

        class ItemType(IntEnum):
            DEFAULT = 0
            ITEM = 1
            TIMER = 2
            POINTS = 3
            MAINTIME = 4
            ATTEMPTS = 5

        class RoundOp(IntEnum):
            NONE = 0
            ROUND = 1
            FLOOR = 2
            CEILING = 3

        class SignOp(IntEnum):
            NONE = 0
            ABSOLUTE = 1
            NEGATIVE = 2

    class Keyframe(IntEnum):
        pass

        class SpinDirection(IntEnum):
            NONE = 0
            CW = 1
            CCW = 2

        class TimeMode(IntEnum):
            TIME = 0
            EVEN = 1
            DIST = 2

    class MoveTargetAxis(IntEnum):
        NONE = 0
        X = 1
        Y = 2

    class OffsetCameraAxis(IntEnum):
        NONE = 0
        X = 1
        Y = 2

    class OffsetGameplayAxis(IntEnum):
        NONE = 0
        X = 1
        Y = 2

    class Options(IntEnum):
        DISABLE = -1
        IGNORE = 0
        ENABLE = 1

    class PickupMode(IntEnum):
        ADD = 0
        MULTIPLY = 1
        DIVIDE = 2

    class PulseTargetType:
        CHANNEL = False
        GROUP = True

    class SequenceMode(IntEnum):
        STOP = 0
        LOOP = 1
        LAST = 2

    class Sfx(IntEnum):
        pass

        class Direction(IntEnum):
            CIRCULAR = 0
            HORIZONTAL = 1
            LEFT = 2
            RIGHT = 3
            VERTICAL = 4
            DOWN = 5
            UP = 6

        class Reverb(IntEnum):
            GENERIC = 0
            PADDED_CELL = 1
            ROOM = 2
            BATH_ROOM = 3
            LIVING_ROOM = 4
            STONE_ROOM = 5
            AUDITORIUM = 6
            CONCERT_HALL = 7
            CAVE = 8
            ARENA = 9
            HANGAR = 10
            STONE_CORRIDOR = 11
            ALLEY = 12
            FOREST = 13
            CITY = 14
            MOUNTAINS = 15
            QUARRY = 16
            PLAIN = 17
            PARKING_LOT = 18
            SEWER_PIPE = 19
            UNDER_WATER = 20

    class ShaderLayer(IntEnum):
        BG = 1
        MG = 2
        B5 = 3
        B4 = 4
        B3 = 5
        B2 = 6
        B1 = 7
        P = 8
        T1 = 9
        T2 = 10
        T3 = 11
        T4 = 12
        G = 13
        UI = 14
        MAX = 15

    class SongDirection(IntEnum):
        CIRCULAR = 0
        HORIZONTAL = 1
        LEFT = 2
        RIGHT = 3
        VERTICAL = 4
        DOWN = 5
        UP = 6

    class StaticCameraAxis(IntEnum):
        NONE = 0
        X = 1
        Y = 2

    class StopMode(IntEnum):
        STOP = 0
        PAUSE = 1
        RESUME = 2

    class TeleportGravity(IntEnum):
        NONE = 0
        NORMAL = 1
        FLIPPED = 2
        TOGGLE = 3

    class Touch(IntEnum):
        pass

        class Mode(IntEnum):
            FLIP = 0
            ON = 1
            OFF = 2

        class OnlyPlayer(IntEnum):
            NONE = 0
            P1 = 1
            P2 = 2

    class UiRefX(IntEnum):
        AUTO = 1
        CENTER = 2
        LEFT = 3
        RIGHT = 4

    class UiRefY(IntEnum):
        AUTO = 1
        CENTER = 2
        BOTTOM = 3
        TOP = 4

class ZLayer(IntEnum):
    B5 = -5
    B4 = -3
    B3 = -1
    DEFAULT = 0
    B2 = 1
    B1 = 3
    T1 = 5
    T2 = 7
    T3 = 9
    T4 = 11
