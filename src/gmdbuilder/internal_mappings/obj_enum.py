from enum import Enum

class ObjEnum(Enum):
    pass

    class Easing(Enum):
        NONE = "a0"
        EASE_IN_OUT = "a1"
        EASE_IN = "a2"
        EASE_OUT = "a3"
        ELASTIC_IN_OUT = "a4"
        ELASTIC_IN = "a5"
        ELASTIC_OUT = "a6"
        BOUNCE_IN_OUT = "a7"
        BOUNCE_IN = "a8"
        BOUNCE_OUT = "a9"
        EXPONENTIAL_IN_OUT = "a10"
        EXPONENTIAL_IN = "a11"
        EXPONENTIAL_OUT = "a12"
        SINE_IN_OUT = "a13"
        SINE_IN = "a14"
        SINE_OUT = "a15"
        BACK_IN_OUT = "a16"
        BACK_IN = "a17"
        BACK_OUT = "a18"

    class ItemLabel(Enum):
        pass

        class Alignment(Enum):
            CENTER = "a0"
            LEFT = "a1"
            RIGHT = "a2"

        class SpecialId(Enum):
            MAINTIME = "a-1"
            POINTS = "a-2"
            ATTEMPTS = "a-3"

    class Level(Enum):
        pass

        class Color17(Enum):
            pass

            class PlayerColor(Enum):
                NONE = "a0"
                PLAYER_1 = "a1"
                PLAYER_2 = "a2"

    class OldColor(Enum):
        PLAYER_1 = "a1"
        PLAYER_2 = "a2"
        COLOR_1 = "a3"
        COLOR_2 = "a4"
        LIGHT_BG = "a5"
        COLOR_3 = "a6"
        COLOR_4 = "a7"
        LINE_3D = "a8"

    class SingleColorType(Enum):
        DEFAULT = "a0"
        BASE = "a1"
        DETAIL = "a2"

    class Trigger(Enum):
        pass

        class AdvFollow(Enum):
            pass

            class Init(Enum):
                INIT = "a0"
                SET = "a1"
                ADD = "a2"

            class Mode(Enum):
                MODE_1 = "a0"
                MODE_2 = "a1"
                MODE_3 = "a2"

        class Arrow(Enum):
            pass

            class Direction(Enum):
                NONE = "a0"
                UP = "a1"
                DOWN = "a2"
                LEFT = "a3"
                RIGHT = "a4"

        class Bpm(Enum):
            pass

            class Speed(Enum):
                NORMAL = "a0"
                SLOW = "a1"
                FAST = "a2"
                VERY_FAST = "a3"
                SUPER_FAST = "a4"

        class CameraEdge(Enum):
            pass

            class Direction(Enum):
                NONE = "a0"
                LEFT = "a1"
                RIGHT = "a2"
                UP = "a3"
                DOWN = "a4"

        class Effect(Enum):
            pass

            class EnterOnly(Enum):
                NONE = "a0"
                ENTER = "a1"
                EXIT = "a2"

            class SpecialCenter(Enum):
                P1 = "a-1"
                P2 = "a-2"
                C = "a-3"
                BL = "a-4"
                CL = "a-5"
                TL = "a-6"
                BC = "a-7"
                TC = "a-8"
                BR = "a-9"
                CR = "a-10"
                TR = "a-11"

        class EnterPreset(Enum):
            pass

            class EnterOnly(Enum):
                NONE = "a0"
                ENTER = "a1"
                EXIT = "a2"

        class Gradient(Enum):
            pass

            class Blending(Enum):
                NORMAL = "a0"
                ADDITIVE = "a1"
                MULTIPLY = "a2"
                INVERT = "a3"

            class Layer(Enum):
                BG = "a1"
                MG = "a2"
                B5 = "a3"
                B4 = "a4"
                B3 = "a5"
                B2 = "a6"
                B1 = "a7"
                P = "a8"
                T1 = "a9"
                T2 = "a10"
                T3 = "a11"
                T4 = "a12"
                G = "a13"
                UI = "a14"
                MAX = "a15"

        class InstantCount(Enum):
            pass

            class Mode(Enum):
                EQUAL = "a0"
                LARGER = "a1"
                SMALLER = "a2"

        class ItemCompare(Enum):
            pass

            class ItemOp(Enum):
                ADD = "a1"
                SUBTRACT = "a2"
                MULTIPLY = "a3"
                DIVIDE = "a4"

            class ItemType(Enum):
                DEFAULT = "a0"
                ITEM = "a1"
                TIMER = "a2"
                POINTS = "a3"
                MAINTIME = "a4"
                ATTEMPTS = "a5"

            class RoundOp(Enum):
                NONE = "a0"
                ROUND = "a1"
                FLOOR = "a2"
                CEILING = "a3"

            class SignOp(Enum):
                NONE = "a0"
                ABSOLUTE = "a1"
                NEGATIVE = "a2"

        class ItemEdit(Enum):
            pass

            class ItemOp(Enum):
                ADD = "a1"
                SUBTRACT = "a2"
                MULTIPLY = "a3"
                DIVIDE = "a4"

            class ItemType(Enum):
                DEFAULT = "a0"
                ITEM = "a1"
                TIMER = "a2"
                POINTS = "a3"
                MAINTIME = "a4"
                ATTEMPTS = "a5"

            class RoundOp(Enum):
                NONE = "a0"
                ROUND = "a1"
                FLOOR = "a2"
                CEILING = "a3"

            class SignOp(Enum):
                NONE = "a0"
                ABSOLUTE = "a1"
                NEGATIVE = "a2"

        class Keyframe(Enum):
            pass

            class SpinDirection(Enum):
                NONE = "a0"
                CW = "a1"
                CCW = "a2"

            class TimeMode(Enum):
                TIME = "a0"
                EVEN = "a1"
                DIST = "a2"

        class Move(Enum):
            pass

            class TargetAxis(Enum):
                NONE = "a0"
                X = "a1"
                Y = "a2"

        class OffsetCamera(Enum):
            pass

            class Axis(Enum):
                NONE = "a0"
                X = "a1"
                Y = "a2"

        class OffsetGameplay(Enum):
            pass

            class Axis(Enum):
                NONE = "a0"
                X = "a1"
                Y = "a2"

        class Options(Enum):
            DISABLE = "a-1"
            IGNORE = "a0"
            ENABLE = "a1"

        class Pickup(Enum):
            pass

            class Mode(Enum):
                ADD = "a0"
                MULTIPLY = "a1"
                DIVIDE = "a2"

        class Pulse(Enum):
            pass

            class TargetType(Enum):
                CHANNEL = "a0"
                GROUP = "a1"

        class Sequence(Enum):
            pass

            class Mode(Enum):
                STOP = "a0"
                LOOP = "a1"
                LAST = "a2"

        class Sfx(Enum):
            pass

            class Direction(Enum):
                CIRCULAR = "a0"
                HORIZONTAL = "a1"
                LEFT = "a2"
                RIGHT = "a3"
                VERTICAL = "a4"
                DOWN = "a5"
                UP = "a6"

            class Reverb(Enum):
                GENERIC = "a0"
                PADDED_CELL = "a1"
                ROOM = "a2"
                BATH_ROOM = "a3"
                LIVING_ROOM = "a4"
                STONE_ROOM = "a5"
                AUDITORIUM = "a6"
                CONCERT_HALL = "a7"
                CAVE = "a8"
                ARENA = "a9"
                HANGAR = "a10"
                STONE_CORRIDOR = "a11"
                ALLEY = "a12"
                FOREST = "a13"
                CITY = "a14"
                MOUNTAINS = "a15"
                QUARRY = "a16"
                PLAIN = "a17"
                PARKING_LOT = "a18"
                SEWER_PIPE = "a19"
                UNDER_WATER = "a20"

        class Shader(Enum):
            pass

            class Layer(Enum):
                BG = "a1"
                MG = "a2"
                B5 = "a3"
                B4 = "a4"
                B3 = "a5"
                B2 = "a6"
                B1 = "a7"
                P = "a8"
                T1 = "a9"
                T2 = "a10"
                T3 = "a11"
                T4 = "a12"
                G = "a13"
                UI = "a14"
                MAX = "a15"

        class Song(Enum):
            pass

            class Direction(Enum):
                CIRCULAR = "a0"
                HORIZONTAL = "a1"
                LEFT = "a2"
                RIGHT = "a3"
                VERTICAL = "a4"
                DOWN = "a5"
                UP = "a6"

        class StaticCamera(Enum):
            pass

            class Axis(Enum):
                NONE = "a0"
                X = "a1"
                Y = "a2"

        class Stop(Enum):
            pass

            class Mode(Enum):
                STOP = "a0"
                PAUSE = "a1"
                RESUME = "a2"

        class Teleport(Enum):
            pass

            class Gravity(Enum):
                NONE = "a0"
                NORMAL = "a1"
                FLIPPED = "a2"
                TOGGLE = "a3"

        class Touch(Enum):
            pass

            class Mode(Enum):
                FLIP = "a0"
                ON = "a1"
                OFF = "a2"

            class OnlyPlayer(Enum):
                NONE = "a0"
                P1 = "a1"
                P2 = "a2"

        class Ui(Enum):
            pass

            class RefX(Enum):
                AUTO = "a1"
                CENTER = "a2"
                LEFT = "a3"
                RIGHT = "a4"

            class RefY(Enum):
                AUTO = "a1"
                CENTER = "a2"
                BOTTOM = "a3"
                TOP = "a4"

    class ZLayer(Enum):
        B5 = "a-5"
        B4 = "a-3"
        B3 = "a-1"
        DEFAULT = "a0"
        B2 = "a1"
        B1 = "a3"
        T1 = "a5"
        T2 = "a7"
        T3 = "a9"
        T4 = "a11"
