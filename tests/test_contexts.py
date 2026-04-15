from pathlib import Path
from gmdbuilder.core import ObjectType
from pytest import raises, ExceptionInfo
from gmdbuilder import (
    autoappend,
    delay,
    groups,
    level_context,
    new_obj,
    obj_prop,
    transform,
    trigger_fn,
    wait,
    Level,
)


def assert_error(exc_info: ExceptionInfo[BaseException], *patterns: str) -> None:
    """Assert exception message contains all patterns (case-insensitive)."""
    msg = str(exc_info.value).lower()
    for pattern in patterns:
        p = pattern.lower()
        assert p in msg, f"Expected '{pattern}' in: {str(exc_info.value)}"


LEVELS_DIR = Path(__file__).parent / "levels"

level = Level.from_file(LEVELS_DIR / "tester.gmd")


class TestGeneralContextManagers:
    def test_autoappend_without_level(self):
        with raises(RuntimeError) as exc_info:
            with autoappend():
                pass
        assert_error(exc_info, "autoappend", "requires", "level_context")

    def test_autoappend_no_double_append(self):
        """Nested autoappend() scopes must not cause the same object to be appended twice."""
        before = len(level.objects)
        with level_context(level):
            with autoappend():
                with autoappend():
                    new_obj(901)
        assert len(level.objects) - before == 1

    def test_transform(self):
        num_calls = 0

        def fn(obj: ObjectType):
            obj[obj_prop.X] = 123
            nonlocal num_calls
            num_calls += 1

        with transform(fn):
            obj1 = new_obj(901)
            obj2 = new_obj(902)

        assert obj1.get(obj_prop.X) == 123, "Transform should have set X=123 on obj1"
        assert obj2.get(obj_prop.X) == 123, "Transform should have set X=123 on obj2"
        assert num_calls == 2, f"Transform called {num_calls} times instead of the expected 2"

    def test_transform_scope_ends(self):
        """Transform must not apply to objects created after the scope exits."""
        applied_to: list[ObjectType] = []

        with transform(lambda obj: applied_to.append(obj)):
            inside = new_obj(901)

        outside = new_obj(1268)

        assert inside in applied_to
        assert outside not in applied_to
        assert len(applied_to) == 1, f"Transform applied to {len(applied_to)} objects"

    def test_groups_accumulate_when_nested(self):
        """Objects created inside nested groups() scopes must carry all enclosing group IDs."""
        with groups(10):
            with groups(20):
                obj = new_obj(901)

        g = set(obj.get(obj_prop.GROUPS) or set())
        assert 10 in g, "Outer group 10 should be present"
        assert 20 in g, "Inner group 20 should be present"

    def test_delay_requires_level_context(self):
        with raises(RuntimeError) as exc_info:
            with delay(1.0):
                pass
        assert_error(exc_info, "delay", "requires", "level_context")

    def test_delay_creates_bridge_and_sub_group(self):
        """
        delay() must append a spawn-bridge trigger to the current context and route
        all objects created inside the block into a freshly allocated sub-group.
        The bridge's TARGET_ID must match the group that inside objects receive.
        """
        before = len(level.objects)

        with level_context(level, autoappend=True):
            with delay(1.5):
                inside = new_obj(901)

        # Two objects appended: the bridge spawn trigger (at delay entry) then the inside object.
        assert len(level.objects) - before == 2

        bridge = level.objects[before]
        assert bridge.get(obj_prop.Trigger.Spawn.DELAY) == 1.5

        # Bridge must target the exact sub-group that the inside object was assigned to.
        bridge_target = bridge.get(obj_prop.Trigger.Spawn.TARGET_ID)
        assert bridge_target in inside.get(obj_prop.GROUPS, set())

    def test_delay_restores_group_after_scope(self):
        """Objects created after a delay() block must not land in the sub-group."""
        with level_context(level, autoappend=True):
            with delay(0.5):
                inside = new_obj(901)
            after = new_obj(901)

        inside_groups = set(inside.get(obj_prop.GROUPS) or set())
        after_groups  = set(after.get(obj_prop.GROUPS) or set())
        inside_groups.remove(9999)
        after_groups.remove(9999)

        # The sub-group used inside the delay block must not appear on the post-delay object.
        assert not inside_groups.intersection(after_groups)


class TestTriggerFunction:
    def test_call_without_level(self):
        @trigger_fn
        def my_trigger():
            pass

        with raises(RuntimeError) as exc_info:
            my_trigger.call()
        assert_error(exc_info, "requires", "active", "level_context")

        with raises(RuntimeError) as exc_info:
            my_trigger()
        assert_error(exc_info, "requires", "active", "level_context")

    def test_objects_empty_before_build(self):
        @trigger_fn
        def fn():
            new_obj(901)

        assert fn.objects == []

    def test_objects_collected(self):
        """Objects created inside the body are captured in .objects."""
        @trigger_fn
        def fn():
            new_obj(901)
            new_obj(1268)

        with level_context(level):
            fn.call()

        assert len(fn.objects) == 2

    def test_objects_appended_to_level(self):
        @trigger_fn
        def fn():
            new_obj(901)

        before = len(level.objects)
        with level_context(level):
            fn.call()

        assert len(level.objects) > before
        assert fn.objects[0] in level.objects

    def test_group_assigned_to_objects(self):
        @trigger_fn
        def fn():
            new_obj(901)

        with level_context(level):
            fn.call()

        for obj in fn.objects:
            assert fn.group in obj.get(obj_prop.GROUPS, set())

    def test_spawn_and_multi_triggered(self):
        @trigger_fn
        def fn():
            new_obj(901)

        with level_context(level):
            fn.call()

        for obj in fn.objects:
            assert obj.get(obj_prop.Trigger.SPAWN_TRIGGER) is True
            assert obj.get(obj_prop.Trigger.MULTI_TRIGGER) is True

    def test_auto_builds_on_first_call(self):
        """First .call() triggers a build if none has occurred yet."""
        @trigger_fn
        def fn():
            new_obj(901)

        assert fn.objects == []
        with level_context(level):
            fn.call()

        assert len(fn.objects) == 1

    def test_no_rebuild_on_subsequent_calls(self):
        """Subsequent .call() invocations do not rebuild — only emit a spawn trigger."""
        @trigger_fn
        def fn():
            new_obj(901)

        with level_context(level):
            fn.call()
            count = len(fn.objects)
            fn.call()
            fn.call()

        assert len(fn.objects) == count

    def test_manual_build(self):
        """fn() builds the trigger function body without creating a spawn trigger."""
        @trigger_fn
        def fn():
            new_obj(901)

        with level_context(level):
            for _ in range(5):
                fn()

        assert len(fn.objects) == 5

    def test_call_skips_build_if_manually_built(self):
        """If fn() was already called, .call() does not rebuild."""
        @trigger_fn
        def fn():
            new_obj(901)

        with level_context(level):
            fn()
            count = len(fn.objects)
            fn.call()

        assert len(fn.objects) == count

    def test_pinned_group(self):
        @trigger_fn(group=500)
        def fn():
            new_obj(901)

        assert fn.group == 500

        with level_context(level):
            fn.call()

        for obj in fn.objects:
            assert 500 in obj.get(obj_prop.GROUPS, set())

    def test_params_invalid_remap_raises(self):
        """Remap keys not declared in params raise ValueError at the .call() site."""
        @trigger_fn(params=[45, 67])
        def fn():
            new_obj(901)

        with level_context(level):
            fn.call()
            with raises(ValueError) as exc_info:
                fn.call(remaps={99: 1})

        assert_error(exc_info, "99", "params")

    def test_params_valid_remap_subset(self):
        """Remapping a subset of declared params does not raise."""
        @trigger_fn(params=[45, 67])
        def fn():
            new_obj(901)

        with level_context(level):
            fn.call()
            fn.call(remaps={45: 100})
            fn.call(remaps={45: 100, 67: 200})

    def test_params_empty_no_remaps_allowed(self):
        """params=[] means any remap raises."""
        @trigger_fn(params=[])
        def fn():
            new_obj(901)

        with level_context(level):
            fn.call()
            with raises(ValueError):
                fn.call(remaps={1: 2})

    def test_spawn_trigger_delay(self):
        """Spawn trigger returned by .call() carries the given delay."""
        @trigger_fn
        def fn():
            new_obj(901)

        with level_context(level):
            spawn = fn.call(delay=1.5)

        assert spawn.get(obj_prop.Trigger.Spawn.DELAY) == 1.5

    def test_spawn_trigger_target(self):
        """Spawn trigger returned by .call() targets the trigger function's group."""
        @trigger_fn
        def fn():
            new_obj(901)

        with level_context(level):
            spawn = fn.call()

        assert spawn.get(obj_prop.Trigger.Spawn.TARGET_ID) == fn.group

    def test_spawn_trigger_remaps(self):
        """Spawn trigger returned by .call(remaps=...) has REMAPS set correctly."""
        @trigger_fn(params=[45])
        def fn():
            new_obj(901)

        with level_context(level):
            fn.call()
            spawn = fn.call(remaps={45: 100})

        assert spawn.get(obj_prop.Trigger.Spawn.REMAPS) == {45: 100}

    def test_spawn_ordered_x_positions(self):
        """In spawn_ordered mode, wait(t) advances X by t * 311.58 for subsequent triggers."""
        @trigger_fn(spawn_ordered=True)
        def fn():
            new_obj(901)
            wait(0.5)
            new_obj(901)

        with level_context(level):
            fn.call()

        assert len(fn.objects) == 2
        x0 = fn.objects[0].get(obj_prop.X, 0.0)
        x1 = fn.objects[1].get(obj_prop.X, 0.0)
        assert x1 > x0
        assert abs(x1 - x0 - 0.5 * 311.58) < 0.01

    def test_non_spawn_ordered_x_increment(self):
        """In default mode, each trigger's X is auto-incremented by 1.3 for execution ordering."""
        @trigger_fn
        def fn():
            new_obj(901)
            new_obj(901)

        with level_context(level):
            fn.call()

        assert len(fn.objects) == 2
        x0 = fn.objects[0].get(obj_prop.X, 0.0)
        x1 = fn.objects[1].get(obj_prop.X, 0.0)
        assert abs(x1 - x0 - 1.0) < 0.01

    def test_definition_time_context(self):
        """Transforms active at decoration time are applied during the build."""
        fired: list[bool] = []

        def record(obj: ObjectType):
            fired.append(True)

        with transform(record):
            @trigger_fn
            def fn():
                new_obj(901)

        with level_context(level):
            fn.call()

        assert len(fired) == 1

    def test_call_time_context_doesnt_bleed_into_body(self):
        """
        Transforms active at .call() time must not reach inside the trigger function body.
        Only the spawn trigger itself (created in the calling context) should be affected.
        """
        applied_to: list[ObjectType] = []

        @trigger_fn
        def fn():
            new_obj(901)
            new_obj(901)

        with level_context(level):
            with transform(lambda obj: applied_to.append(obj)):
                fn.call()

        # fn body produces 2 objects; the calling-context transform must not touch them.
        assert len(fn.objects) == 2
        # Exactly one object should have been caught by the call-time transform:
        # the spawn trigger that .call() itself creates in the calling context.
        assert len(applied_to) == 1
        assert applied_to[0] not in fn.objects

    def test_delay_context(self):
        """
        delay() inside a trigger function body must:
          - keep the first object in the trigger function's entry group
          - create a spawn bridge in the entry group with the correct delay
          - route objects inside the with-block into a separate sub-group
          - have the bridge's TARGET_ID match that sub-group
        """
        @trigger_fn
        def fn():
            new_obj(901)       # [0] Move — belongs to entry group
            with delay(2.5):   # bridge spawn trigger appended as [1]
                new_obj(1268)  # [2] Spawn — belongs to sub-group

        with level_context(level):
            fn.call()

        # Ordering: Move(901) → bridge spawn (from delay entry) → inside Spawn(1268)
        assert len(fn.objects) == 3

        # [0] Move is in the trigger function's entry group
        assert fn.group in fn.objects[0].get(obj_prop.GROUPS, set())

        # [1] Bridge spawn trigger is also in the entry group (created before group switch)
        assert fn.group in fn.objects[1].get(obj_prop.GROUPS, set())
        assert fn.objects[1].get(obj_prop.Trigger.Spawn.DELAY) == 2.5

        # [2] Object inside the delay block is NOT in the entry group
        assert fn.group not in fn.objects[2].get(obj_prop.GROUPS, set())

        # Bridge must target the sub-group that [2] belongs to
        sub_group = fn.objects[1].get(obj_prop.Trigger.Spawn.TARGET_ID)
        assert sub_group in fn.objects[2].get(obj_prop.GROUPS, set())