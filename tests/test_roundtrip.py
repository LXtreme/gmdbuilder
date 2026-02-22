"""
Roundtrip tests: load a level, append an object, save to a new file, reload.
Parametrized over every .gmd file found in tests/levels/.
"""

import pytest
from pathlib import Path

import gmdbuilder.level as _level_module
from gmdbuilder import level
from gmdbuilder.core import new_object
from gmdbuilder.mappings import obj_prop
from gmdbuilder.validation import setting

setting.export.spawn_limit_check = False

LEVELS_DIR = Path(__file__).parent / "levels"
LEVEL_FILES = sorted(LEVELS_DIR.glob("*.gmd"))

def _reset_level() -> None:
    """Wipe all module-level state so the next from_file() call is clean."""
    _level_module._kit_level = None # type: ignore
    _level_module._source_file = None # type: ignore
    _level_module._live_editor = None # type: ignore
    _level_module.objects = _level_module.ObjectList(live_editor=False)
    _level_module.tag_group = 9999
    _level_module.new.reset_all()


@pytest.fixture(autouse=True)
def clean_level_state():
    """Ensure a clean module state before *and* after every test."""
    _reset_level()
    yield
    _reset_level()


# ── Tests ─────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("level_file", LEVEL_FILES, ids=lambda p: p.name)
def test_roundtrip(level_file: Path, tmp_path: Path) -> None:

    # 1. Load the original level file.
    level.from_file(level_file)
    initial_count = len(level.objects)

    # 2. Create and append a move trigger.
    obj = new_object(901)
    obj[obj_prop.X] = 100
    obj[obj_prop.Y] = 100
    obj[obj_prop.Trigger.Move.DURATION] = 1.0
    obj[obj_prop.Trigger.Move.TARGET_ID] = 1
    level.objects.append(obj)

    assert len(level.objects) == initial_count + 1, (
        "Object count should increase by exactly 1 after append"
    )

    # 3. Save into a new file (never touches the original).
    out_file = tmp_path / level_file.name
    level.export_to_file(out_file)

    assert out_file.exists(), "Export should have created the output file"

    # 4. Load the updated file.
    # The appended object received tag_group 9999 at export time, so it is
    # filtered back out on load — the count should be back to initial_count.
    _reset_level()
    level.from_file(out_file)

    assert len(level.objects) == initial_count, (
        "After reload, the tagged object should be filtered out and the "
        "count should match the original"
    )