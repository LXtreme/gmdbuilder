import pytest

from gmdbuilder.classes import ItemCompare, ItemEdit
from gmdbuilder.mappings.obj_enum import Item


def test_edit_basic():
    e = ItemEdit().set_from_string("i12 = (t2 + i3) * 4")
    assert (e.target_item_id, e.target_item_type) == (12, Item.ItemType.ITEM)
    assert (e.item_id_1, e.item_type_1) == (2, Item.ItemType.TIMER)
    assert (e.item_id_2, e.item_type_2) == (3, Item.ItemType.ITEM)
    assert e.item_op_1 == Item.MathOp.ASSIGN
    assert e.item_op_2 == Item.MathOp.ADD
    assert e.item_op_3 == Item.MathOp.MULTIPLY
    assert e.mod == 4.0


def test_edit_funcs_and_assign():
    e = ItemEdit().set_from_string("i5 += abs(floor(i1 / 2))")
    assert e.item_op_1 == Item.MathOp.ADD
    assert e.item_op_3 == Item.MathOp.DIVIDE
    assert e.round_op_1 == Item.RoundOp.FLOOR
    assert e.sign_op_1 == Item.SignOp.ABSOLUTE
    e = ItemEdit().set_from_string("ceil(p *= a)")
    assert e.target_item_type == Item.ItemType.POINTS
    assert e.item_type_1 == Item.ItemType.ATTEMPTS
    assert e.round_op_2 == Item.RoundOp.CEILING


@pytest.mark.parametrize("s", [
    "i12 = t2 + 4.0",
    "i1 = i2 / 0",
    "m = i1",
    "a = i1",
    "i1 = i2 + i3 + i4",
    "i1 = i2 + i3 * 2",
    "i1 = floor(abs(i2))",
    "i1 = 5",
    "",
])
def test_edit_rejects(s):
    with pytest.raises(ValueError):
        ItemEdit().set_from_string(s)


def test_compare():
    c = ItemCompare().set_from_string("abs(floor(i1 / 2)) <= 5")
    assert c.item_op_3 == Item.CompareOp.LTE
    assert c.item_op_1 == Item.MathOp.DIVIDE and c.mod_1 == 2.0
    assert c.round_op_1 == Item.RoundOp.FLOOR and c.sign_op_1 == Item.SignOp.ABSOLUTE
    assert c.item_type_2 == Item.ItemType.DEFAULT and c.mod_2 == 5.0
    c = ItemCompare().set_from_string("t3 + 1 != p")
    assert c.item_op_3 == Item.CompareOp.NE
    assert c.item_type_2 == Item.ItemType.POINTS


@pytest.mark.parametrize("s", ["i1 + i2 > 3", "i1 / 0 > 1", "i1", "i1 = 2"])
def test_compare_rejects(s):
    with pytest.raises(ValueError):
        ItemCompare().set_from_string(s)
