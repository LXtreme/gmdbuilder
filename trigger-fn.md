# trigger_fn design

```python
from gmdbuilder import Level, trigger_fn, wait, order, level_context, autoappend
from gmdbuilder import new_obj, obj_prop, obj_id
from gmdbuilder.classes import Move, Count, Spawn

level = Level.from_file("example.gmd")


# --- Basic trigger function ---
# All triggers inside are automatically spawn_triggered and multi_triggered.
# Group is auto-allocated on first access of .group or on first .call(),
# whichever comes first. Requires active level_context at that point.
#
# In regular mode, each trigger created inside the function is automatically
# placed at X += 1.3 units ahead of the previous one within the same group.
# This guarantees sub-tick execution order matches creation order without
# relying on object-string position.

@trigger_fn
def move_right():
    m = Move()
    m.target_id = 45
    m.move_x = 100
    m.duration = 0.5


# --- order() context manager ---
# Sets the ordering mode for wait() calls within its scope.
# Can be used as a standalone context manager or via spawn_ordered= on @trigger_fn.
# @trigger_fn(spawn_ordered=True) is shorthand for wrapping the entire body in
# order(spawn_ordered=True).
#
# order(spawn_ordered=True):
#   wait(t) advances the X offset of subsequent triggers by t * 311.58 units
#   (GD's 1x speed constant). No implicit X stepping between triggers —
#   same-X triggers are ordered by object-string position (i.e. creation order).
#   Advantage: no extra groups or spawn triggers needed for timing.
#   Tradeoff: timing is baked into X positions at build time.
#
# Regular mode (default / order(spawn_ordered=False)):
#   wait(t) allocates a new group, chained via a spawn trigger with the given delay.
#   Triggers within each group are auto-spaced by X += 1.3 for subtick ordering.

@trigger_fn(spawn_ordered=True)
def move_bounce():
    m = Move()
    m.target_id = 45
    m.move_x = 100
    m.duration = 0.5
    wait()        # X offset += 1.3 (one tick gap, subtick ordering only)
    wait(0.5)     # X offset += 0.5 * 311.58 units; all subsequent triggers shift forward
    m2 = Move()
    m2.target_id = 45
    m2.move_x = -100
    m2.duration = 0.5


# --- Regular mode wait() ---
# wait(t) allocates a new group and chains it to the current one via a spawn trigger
# with the given delay. Triggers placed after wait() belong to the new group.
# Sub-groups are managed transparently — callers never need to track them.
# Within each group, triggers are auto-spaced by X += 1.3 for subtick ordering.
#
# wait() with no argument:
#   Spawn-ordered mode: X offset += 1.3 (one tick gap, subtick ordering only).
#   Regular mode: TBD — either a delay-0 spawn chain or an X-only step.

@trigger_fn
def move_then_count():
    m = Move()
    m.target_id = 45
    m.move_x = 100
    m.duration = 0.5
    wait(0.5)    # new group allocated, spawn trigger added with delay=0.5
    c = Count()  # belongs to the new group
    c.item_id = 10
    c.count = 1


# --- Pinned group ---
# Use group= to bind to a known ID.
# Useful when other level content already references this group by hand.
# .group is available immediately without needing level_context.

@trigger_fn(group=5)
def pinned_fn():
    m = Move()
    m.target_id = 45
    m.move_x = 50


# --- params: required remap list ---
# params declares which group IDs must appear in the remap dict on every .call().
# ALL listed IDs must be included — omitting any one raises ValueError at the call site.
# Extra remap keys beyond those listed in params are silently accepted.
# Omitting params entirely disables validation — any remap dict (or none) is accepted.

@trigger_fn(spawn_ordered=True, params=[45, 67])
def two_targets():
    m = Move()
    m.target_id = 45
    m.move_x = 100
    m.duration = 0.5
    wait(0.5)
    m2 = Move()
    m2.target_id = 67
    m2.move_x = -100
    m2.duration = 0.5


# --- .call() ---
# The build phase runs on the first .call() (or first .group access) per level.
# Both level_context and autoappend must be active at build time.
# RuntimeError if either is missing.
#
# Requiring autoappend at build time keeps the build path unambiguous:
# all trigger function internals go through the same validated append route,
# with no risk of objects being missed, duplicated, or appended to the wrong level.
#
# .call() always returns the spawn trigger it creates.
# If autoappend is active at the call site, the spawn trigger is appended automatically.
# If not, the returned spawn trigger can be modified and appended manually.
# Subsequent .call() invocations after the build do not require autoappend.

with level_context(level):
    with autoappend():
        move_right.call()            # build + spawn trigger appended, delay=0
        move_right.call(delay=2.0)   # spawn trigger appended, delay=2.0

        two_targets.call(remap={45: 100, 67: 200})           # all params remapped ✓
        two_targets.call(remap={45: 100, 67: 200, 99: 300})  # extra key ok ✓
        # two_targets.call()                 # ValueError: params [45, 67] must be remapped
        # two_targets.call(remap={45: 100})  # ValueError: 67 missing from remap

# Calling outside autoappend — spawn trigger returned for manual handling.
# Build already happened above so no level_context needed here.
sp = move_right.call()  # spawn trigger not auto-appended
sp[obj_prop.X] = 300    # modify before appending manually
level.objects.append(sp)

# .group is an IntEnum, usable anywhere a plain int group ID is expected
s = Spawn()
s.target_id = move_right.group  # already allocated from the .call() above
s.delay = 1.0


# --- Context capture ---
# @trigger_fn captures the active ContextVar state at definition time.
# At build time, the body runs inside that captured context, with the function's
# own fn_group overlaid on top. Context managers active at definition time —
# such as groups(), order(), or custom transforms — are inherited by the body.
#
# The spawn trigger emitted by .call() inherits the context active at the call site,
# independently of the definition-time context.

with groups(debug_g):
    @trigger_fn
    def move_debug():
        m = Move()      # in {fn_group, debug_g} at build time — debug_g captured
        m.target_id = 45
        m.move_x = 50

with level_context(level), autoappend():
    move_debug.call()   # spawn trigger inherits call-site context, not definition-time context


# --- Nesting ---
# Trigger functions can call other trigger functions inside their body.
# inner only needs to be defined by the time outer.call() is first invoked, not before.
# If inner has not been built yet when outer's body runs, it is built at that point
# using inner's own captured definition-time context — not outer's build context.

@trigger_fn
def inner():
    c = Count()
    c.item_id = 1
    c.count = 1

@trigger_fn
def outer():
    m = Move()
    m.target_id = 10
    m.move_x = 50
    wait(0.3)
    inner.call()         # emits a spawn trigger to inner.group inside outer's chain
    inner.call(delay=1)  # call it again later


# --- Parameterized variants: generator pattern ---
# @trigger_fn does not support runtime parameters on the function itself.
# Wrap in a normal Python function to bake script-time values into separate,
# independent trigger functions. Each factory call produces its own group.
# Type checking on the factory's parameters works as normal.

def make_mover(target: int, amount: int):
    @trigger_fn
    def _fn():
        m = Move()
        m.target_id = target   # baked in at factory-call time, no placeholder IDs
        m.move_x = amount
        m.duration = 0.5
    return _fn

mover_a = make_mover(target=45, amount=100)   # owns its own group
mover_b = make_mover(target=67, amount=-100)  # completely independent group

with level_context(level), autoappend():
    mover_a.call()
    mover_b.call(delay=1.0)
    mover_a.call(delay=2.0)  # calls the already-built mover_a again


# --- Properties ---

move_right.group    # IntEnum — the allocated group ID.
                    # For @trigger_fn(group=5): available immediately.
                    # For auto-allocated: lazily calls level.new.group() on first access.
                    # Raises RuntimeError if accessed without active level_context
                    # before first allocation.

move_right.params   # list[int] | None — required remap keys.
                    # None if params was not specified (no validation enforced).

move_right.objects  # list[ObjectType] — every object built into this function,
                    # including objects in sub-groups created by wait().
                    # Empty list before first .call().
```
