from typing import Self

from gmdbuilder.classes import _item_expr
from gmdbuilder.classes.object import ObjField
from gmdbuilder.classes.trigger import Trigger
from gmdbuilder.mappings import obj_id, obj_prop
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
    # Methods
    # ------------------------------------------------------------------

    def set_from_string(self, expr: str) -> Self:
        """
        Fill in the comparison properties from a string such as ``"i1 * 2 >= t3 + 1"``.

        Operands: ``i<ID>`` item, ``t<ID>`` timer, ``p`` points, ``m`` main time,
        ``a`` attempts, or a bare number (constant).

        Each side is ONE operand with an optional constant: ``i1``, ``i1 + 2``,
        ``t3 * 0.5``, or just ``5``. Two operands on one side (``i1 + i2``) are
        not possible in Item Compare. Comparison is one of ``== != < <= > >=``.

        Each side can be wrapped in a rounding function (``round``/``floor``/``ceil``)
        and a sign function (``abs``/``neg``), sign outermost since GD applies it
        after rounding: ``abs(floor(i1 / 2)) < 4``.

        Does not touch ``true_id``, ``false_id`` or ``tolerance``.
        Raises ``ValueError`` for anything GD cannot represent.
        """
        spec = _item_expr.parse_compare(expr)
        l, r = spec.left, spec.right
        self.item_id_1, self.item_type_1 = l.item.id, l.item.type
        self.item_id_2, self.item_type_2 = r.item.id, r.item.type
        self.item_op_1, self.mod_1 = l.op, l.mod
        self.item_op_2, self.mod_2 = r.op, r.mod
        self.item_op_3 = spec.cmp
        self.round_op_1, self.sign_op_1 = l.funcs.round, l.funcs.sign
        self.round_op_2, self.sign_op_2 = r.funcs.round, r.funcs.sign
        return self

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

    def set_from_string(self, expr: str) -> Self:
        """
        Fill in the item edit properties from a string such as ``"i12 = (t2 + i3) * 4"``.

        Form: ``<target> <assign> <rhs>`` where target is ``i<ID>``, ``t<ID>`` or ``p``
        (main time and attempts are read-only) and assign is ``= += -= *= /=``.

        The right-hand side is GD's fixed shape ``(I1 [+ - * /] I2) [* /] mod``:
        ``i1``, ``i1 - i2``, ``i1 * 3``, ``(i1 + i2) / 2``, ``i1 * i2 * 0.5``.
        Operands: ``i<ID>``, ``t<ID>``, ``p`` points, ``m`` main time, ``a`` attempts.

        NOT possible: adding/subtracting a constant (Mod only multiplies or divides,
        so ``i12 = t2 + 4.0`` is rejected; use a Pickup trigger), more than two operands,
        and dividing by 0.

        The rhs may be wrapped in rounding (``round``/``floor``/``ceil``) and sign
        (``abs``/``neg``) functions, sign outermost: ``i1 = abs(floor(i2 / 2))``.
        Wrapping the whole statement instead (``floor(i1 += i2)``) applies them to the
        assignment result.

        Raises ``ValueError`` for anything GD cannot represent.
        """
        s = _item_expr.parse_edit(expr)
        self.target_item_id, self.target_item_type = s.target.id, s.target.type
        self.item_id_1, self.item_type_1 = s.item_1.id, s.item_1.type
        self.item_id_2, self.item_type_2 = s.item_2.id, s.item_2.type
        self.item_op_1 = s.assign_op
        self.item_op_2 = s.param_op
        self.item_op_3 = s.mod_op
        self.mod = s.mod
        self.round_op_1, self.sign_op_1 = s.mod_funcs.round, s.mod_funcs.sign
        self.round_op_2, self.sign_op_2 = s.out_funcs.round, s.out_funcs.sign
        return self

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    target_item_id = ObjField[int](obj_prop.Trigger.ItemEdit.TARGET_ITEM_ID)
    """Item ID to write the result into (a51)"""

    target_item_type = ObjField[Item.ItemType](obj_prop.Trigger.ItemEdit.TARGET_ITEM_TYPE)
    """Type of target item: DEFAULT/ITEM/TIMER/POINTS/MAINTIME/ATTEMPTS (a478)"""

    item_id_1 = ObjField[int](obj_prop.Trigger.ItemEdit.ITEM_ID_1)
    """First source item ID (a80)"""

    item_id_2 = ObjField[int](obj_prop.Trigger.ItemEdit.ITEM_ID_2)
    """Second source item ID (a95)"""

    item_type_1 = ObjField[Item.ItemType](obj_prop.Trigger.ItemEdit.ITEM_TYPE_1)
    """Type of item 1: DEFAULT/ITEM/TIMER/POINTS/MAINTIME/ATTEMPTS (a476)"""

    item_type_2 = ObjField[Item.ItemType](obj_prop.Trigger.ItemEdit.ITEM_TYPE_2)
    """Type of item 2: DEFAULT/ITEM/TIMER/POINTS/MAINTIME/ATTEMPTS (a477)"""

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