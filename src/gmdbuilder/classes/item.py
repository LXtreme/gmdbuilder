
from gmdbuilder.classes.object import ObjField
from gmdbuilder.classes.trigger import Trigger
from gmdbuilder.mappings import obj_prop, obj_id
from gmdbuilder.mappings.obj_enum import InstantCountMode, Item, PickupMode


class Pickup(Trigger):
    """Pickup trigger. Inherits: Object -> Trigger -> Pickup"""

    def __init__(self):
        super().__init__(obj_id.Trigger.PICKUP)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    count = ObjField[int](obj_prop.Trigger.Pickup.COUNT)
    """Amount to add/multiply/divide the item by (a77)"""

    item_id = ObjField[int](obj_prop.Trigger.Pickup.ITEM_ID)
    """Item ID to modify (a80)"""

    mode = ObjField[PickupMode](obj_prop.Trigger.Pickup.MODE)
    """Operation mode: ADD / MULTIPLY / DIVIDE (a88)"""

    override = ObjField[bool](obj_prop.Trigger.Pickup.OVERRIDE)
    """Set item to count instead of applying the operation (a139)"""

    mod = ObjField[float](obj_prop.Trigger.Pickup.MOD)
    """Float modifier applied alongside count (a449)"""


class Count(Trigger):
    """Count trigger. Inherits: Object -> Trigger -> Count"""

    def __init__(self):
        super().__init__(obj_id.Trigger.COUNT)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    target_id = ObjField[int](obj_prop.Trigger.Count.TARGET_ID)
    """Group ID to activate when count is reached (a51)"""

    activate_group = ObjField[bool](obj_prop.Trigger.Count.ACTIVATE_GROUP)
    """True = activate group, False = deactivate (a56)"""

    count = ObjField[int](obj_prop.Trigger.Count.COUNT)
    """Item count value to trigger at (a77)"""

    item_id = ObjField[int](obj_prop.Trigger.Count.ITEM_ID)
    """Item ID to watch (a80)"""

    multi_activate = ObjField[bool](obj_prop.Trigger.Count.MULTI_ACTIVATE)
    """Trigger every time count is reached, not just the first (a104)"""


class InstantCount(Trigger):
    """Instant Count trigger. Inherits: Object -> Trigger -> InstantCount"""

    def __init__(self):
        super().__init__(obj_id.Trigger.INSTANT_COUNT)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    target_id = ObjField[int](obj_prop.Trigger.InstantCount.TARGET_ID)
    """Group ID to activate (a51)"""

    activate_group = ObjField[bool](obj_prop.Trigger.InstantCount.ACTIVATE_GROUP)
    """True = activate group, False = deactivate (a56)"""

    count = ObjField[int](obj_prop.Trigger.InstantCount.COUNT)
    """Item count value to compare against (a77)"""

    item_id = ObjField[int](obj_prop.Trigger.InstantCount.ITEM_ID)
    """Item ID to check (a80)"""

    mode = ObjField[InstantCountMode](obj_prop.Trigger.InstantCount.MODE)
    """Comparison mode: EQUAL / LARGER / SMALLER (a88)"""


class ItemCompare(Trigger):
    """Item Compare trigger. Inherits: Object -> Trigger -> ItemCompare"""

    def __init__(self):
        super().__init__(obj_id.Trigger.ITEM_COMPARE)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    true_id = ObjField[int](obj_prop.Trigger.ItemCompare.TRUE_ID)
    """Group ID to spawn when comparison is true (a51)"""

    false_id = ObjField[int](obj_prop.Trigger.ItemCompare.FALSE_ID)
    """Group ID to spawn when comparison is false (a71)"""

    item_id_1 = ObjField[int](obj_prop.Trigger.ItemCompare.ITEM_ID_1)
    """First item ID (a80)"""

    item_id_2 = ObjField[int](obj_prop.Trigger.ItemCompare.ITEM_ID_2)
    """Second item ID (a95)"""

    item_type_1 = ObjField[Item.ItemType](obj_prop.Trigger.ItemCompare.ITEM_TYPE_1)
    """Type of item 1: DEFAULT/ITEM/TIMER/POINTS/MAINTIME/ATTEMPTS (a476)"""

    item_type_2 = ObjField[Item.ItemType](obj_prop.Trigger.ItemCompare.ITEM_TYPE_2)
    """Type of item 2: DEFAULT/ITEM/TIMER/POINTS/MAINTIME/ATTEMPTS (a477)"""

    mod_1 = ObjField[float](obj_prop.Trigger.ItemCompare.MOD_1)
    """Multiplier applied to item 1 before comparison (a479)"""

    item_op_1 = ObjField[Item.MathOp](obj_prop.Trigger.ItemCompare.ITEM_OP_1)
    """Operation applied to item 1: ADD/SUBTRACT/MULTIPLY/DIVIDE (a480)"""

    item_op_2 = ObjField[Item.MathOp](obj_prop.Trigger.ItemCompare.ITEM_OP_2)
    """Operation applied to item 2: ADD/SUBTRACT/MULTIPLY/DIVIDE (a481)"""

    item_op_3 = ObjField[Item.MathOp](obj_prop.Trigger.ItemCompare.ITEM_OP_3)
    """Comparison operator between the two results (a482)"""

    mod_2 = ObjField[float](obj_prop.Trigger.ItemCompare.MOD_2)
    """Multiplier applied to item 2 before comparison (a483)"""

    tolerance = ObjField[float](obj_prop.Trigger.ItemCompare.TOLERANCE)
    """Tolerance range for equality comparison (a484)"""

    round_op_1 = ObjField[Item.RoundOp](obj_prop.Trigger.ItemCompare.ROUND_OP_1)
    """Rounding applied to item 1: NONE/ROUND/FLOOR/CEILING (a485)"""

    round_op_2 = ObjField[Item.RoundOp](obj_prop.Trigger.ItemCompare.ROUND_OP_2)
    """Rounding applied to item 2: NONE/ROUND/FLOOR/CEILING (a486)"""

    sign_op_1 = ObjField[Item.SignOp](obj_prop.Trigger.ItemCompare.SIGN_OP_1)
    """Sign operation on item 1: NONE/ABSOLUTE/NEGATIVE (a578)"""

    sign_op_2 = ObjField[Item.SignOp](obj_prop.Trigger.ItemCompare.SIGN_OP_2)
    """Sign operation on item 2: NONE/ABSOLUTE/NEGATIVE (a579)"""


class ItemEdit(Trigger):
    """Item Edit trigger. Inherits: Object -> Trigger -> ItemEdit"""

    def __init__(self):
        super().__init__(obj_id.Trigger.ITEM_EDIT)

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------


    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    target_item_id = ObjField[int](obj_prop.Trigger.ItemEdit.TARGET_ITEM_ID)
    """Item ID to write the result into (a51)"""

    item_id_1 = ObjField[int](obj_prop.Trigger.ItemEdit.ITEM_ID_1)
    """First source item ID (a80)"""

    item_id_2 = ObjField[int](obj_prop.Trigger.ItemEdit.ITEM_ID_2)
    """Second source item ID (a95)"""

    item_type_1 = ObjField[Item.ItemType](obj_prop.Trigger.ItemEdit.ITEM_TYPE_1)
    """Type of item 1: DEFAULT/ITEM/TIMER/POINTS/MAINTIME/ATTEMPTS (a476)"""

    item_type_2 = ObjField[Item.ItemType](obj_prop.Trigger.ItemEdit.ITEM_TYPE_2)
    """Type of item 2: DEFAULT/ITEM/TIMER/POINTS/MAINTIME/ATTEMPTS (a477)"""

    item_type_3 = ObjField[Item.ItemType](obj_prop.Trigger.ItemEdit.ITEM_TYPE_3)
    """Type of target item: DEFAULT/ITEM/TIMER/POINTS/MAINTIME/ATTEMPTS (a478)"""

    mod = ObjField[float](obj_prop.Trigger.ItemEdit.MOD)
    """Float modifier applied in the operation (a479)"""

    item_op_1 = ObjField[Item.MathOp](obj_prop.Trigger.ItemEdit.ITEM_OP_1)
    """Operation between item 1 and mod: ADD/SUBTRACT/MULTIPLY/DIVIDE (a480)"""

    item_op_2 = ObjField[Item.MathOp](obj_prop.Trigger.ItemEdit.ITEM_OP_2)
    """Operation between item 2 and the result of op1: ADD/SUBTRACT/MULTIPLY/DIVIDE (a481)"""

    item_op_3 = ObjField[Item.MathOp](obj_prop.Trigger.ItemEdit.ITEM_OP_3)
    """Final operation applied before writing to target (a482)"""

    round_op_1 = ObjField[Item.RoundOp](obj_prop.Trigger.ItemEdit.ROUND_OP_1)
    """Rounding on item 1 result: NONE/ROUND/FLOOR/CEILING (a485)"""

    round_op_2 = ObjField[Item.RoundOp](obj_prop.Trigger.ItemEdit.ROUND_OP_2)
    """Rounding on item 2 result: NONE/ROUND/FLOOR/CEILING (a486)"""

    sign_op_1 = ObjField[Item.SignOp](obj_prop.Trigger.ItemEdit.SIGN_OP_1)
    """Sign operation on item 1: NONE/ABSOLUTE/NEGATIVE (a578)"""

    sign_op_2 = ObjField[Item.SignOp](obj_prop.Trigger.ItemEdit.SIGN_OP_2)
    """Sign operation on item 2: NONE/ABSOLUTE/NEGATIVE (a579)"""


class ItemPersist(Trigger):
    """Item Persist trigger. Inherits: Object -> Trigger -> ItemPersist"""

    def __init__(self):
        super().__init__(obj_id.Trigger.ITEM_PERSIST)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    item_id = ObjField[int](obj_prop.Trigger.ItemPersist.ITEM_ID)
    """Item ID to persist (a80)"""

    set_persistent = ObjField[bool](obj_prop.Trigger.ItemPersist.SET_PERSISTENT)
    """Enable persistence across attempts (a491)"""

    target_all = ObjField[bool](obj_prop.Trigger.ItemPersist.TARGET_ALL)
    """Apply to all item IDs (a492)"""

    reset = ObjField[bool](obj_prop.Trigger.ItemPersist.RESET)
    """Reset the persisted value (a493)"""

    timer = ObjField[bool](obj_prop.Trigger.ItemPersist.TIMER)
    """Persist timer rather than item counter (a494)"""