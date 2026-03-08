"""
Roundtrip tests: load a level, append an object, save to a new file, reload.
Parametrized over every .gmd file found in tests/levels/.
"""

import pytest
from pathlib import Path

from gmdbuilder.color import Color
from gmdbuilder.level import Level
from gmdbuilder.core import new_obj
from gmdbuilder.mappings import obj_prop
from gmdbuilder.validation import setting

setting.spawn_limit_check = False

LEVELS_DIR = Path(__file__).parent / "levels"
LEVEL_FILES = sorted(LEVELS_DIR.glob("*.gmd"))


# ── Tests ─────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("level_file", LEVEL_FILES, ids=lambda p: p.name)
def test_roundtrip(level_file: Path, tmp_path: Path) -> None:

    level = Level.from_file(level_file)
    initial_count = len(level.objects)

    # 1. Append a new object — it gets tag_group applied automatically.
    obj = new_obj(901)
    obj[obj_prop.X] = 123
    obj[obj_prop.Y] = 321
    obj[obj_prop.Trigger.Move.DURATION] = 1.0
    obj[obj_prop.Trigger.Move.TARGET_ID] = 1
    level.objects.append(obj)

    assert len(level.objects) == initial_count + 1, (
        "Object count should increase by exactly 1 after append"
    )

    c = level.new.color()
    level.color[c] = Color(red=255, green=128, blue=64, opacity=0.5, blending=True)

    g = level.new.group()
    level.objects[0][obj_prop.GROUPS] = {int(g)}

    out_file = tmp_path / level_file.name
    level.export_to_file(out_file)

    assert out_file.exists(), "Export should have created the output file"

    level = Level.from_file(out_file)

    assert len(level.objects) == initial_count, (
        "After reload, the tagged object should be filtered out and the "
        "count should match the original"
    )

    assert c in level.color, f"Color channel {c} should be present after reload"
    
    col = level.color[c]
    assert col.red == 255,      f"Expected red=255,     got {col.red}"
    assert col.green == 128,    f"Expected green=128,   got {col.green}"
    assert col.blue == 64,      f"Expected blue=64,     got {col.blue}"
    assert col.opacity == 0.5,  f"Expected opacity=0.5, got {col.opacity}"
    assert col.blending is True, f"Expected blending=True, got {col.blending}"

    # 7. Group g should still be assigned to at least one object after reload.
    obj_with_g = next(
        (o for o in level.objects if int(g) in o.get(obj_prop.GROUPS, set())),
        None,
    )
    assert obj_with_g is not None, (
        f"Expected at least one object to carry group {int(g)} after reload"
    )