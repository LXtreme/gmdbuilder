# trigger_fn design

```python
from gmdbuilder import Level, trigger_fn, wait, level_context, autoappend
from gmdbuilder import new_obj, obj_prop, obj_id
from gmdbuilder.classes import Move, Count, Spawn

level = Level.from_file("example.gmd")


# --- Basic trigger function ---
# All triggers inside are automatically spawn_triggered and multi_triggered.
# Group is auto-allocated on first access of .group or on first .call(),
# whichever comes first. Requires active level_context at that point.

@trigger_fn
def move_right():
    m = Move()
    m.target_id = 45
    m.move_x = 100
    m.duration = 0.5


# --- spawn_ordered mode ---
# All triggers share a single group, sequenced by X position rather than spawn delay chains.
# wait(t) advances the X offset by t * 311.58 units (GD's 1x speed constant).
# More efficient than regular mode: no extra groups or spawn triggers needed for timing.
# Tradeoff: timing is baked into X positions at build time and cannot be remapped at runtime.
#
# Triggers with the same logical time share the same X position.
# No micro-gaps are added automatically — sub-tick ordering for same-X triggers
# is determined by their order in the level's object string (i.e. order of creation).
# Explicit wait() is the only way to advance time.

@trigger_fn(spawn_ordered=True)
def move_bounce():
    m = Move()
    m.target_id = 45
    m.move_x = 100
    m.duration = 0.5
    wait() # x offset += 1.3
    wait(0.5)       # X offset += 0.5 * 311.58 units for all subsequent triggers
    m2 = Move()
    m2.target_id = 45
    m2.move_x = -100
    m2.duration = 0.5


# --- Regular mode wait() ---
# wait(t) allocates a new group and chains it to the current one via a spawn trigger
# with the given delay. Triggers placed after wait() belong to the new group.
# Sub-groups are managed transparently — callers never need to track them.
# Sub-tick ordering without wait() is determined by X position, then object string order.

@trigger_fn
def move_then_count():
    m = Move()
    m.target_id = 45
    m.move_x = 100
    m.duration = 0.5
    wait(0.5)       # new group allocated, spawn trigger added with delay=0.5
    c = Count()     # belongs to the new group
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


# --- params: remap allowlist ---
# params declares which group IDs inside the function are valid remap targets.
# Passing a key not in params raises ValueError at the .call() site.
# Omitting params entirely means any remap is allowed — no validation.

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
# The build phase (first .call()) requires level_context and autoappend to be active.
# RuntimeError if either is missing at that point.
#
# .call() always returns the spawn trigger it creates.
# If autoappend is active at the call site, the spawn trigger is appended automatically.
# If not, the returned spawn trigger can be appended or modified manually.
# This means subsequent .call() invocations after the first do not strictly require autoappend.

with level_context(level):
    with autoappend():

        move_right.call()               # build + spawn trigger appended, delay=0
        move_right.call(delay=2.0)      # spawn trigger appended, delay=2.0

        two_targets.call()                          # no remap, 45 and 67 used as-is
        two_targets.call(remap={45: 100})           # remapping one is fine
        two_targets.call(remap={45: 100, 67: 200})  # remap both
        # two_targets.call(remap={99: 1})           # ValueError: 99 not in params=[45, 67]

# calling outside of autoappend — spawn trigger returned for manual handling
sp = move_right.call()  # spawn trigger not auto-appended
sp[obj_prop.X] = 300    # modify before appending manually
level.objects.append(sp)

# .group is an IntEnum, usable anywhere a plain int group ID is expected
s = Spawn()
s.target_id = move_right.group  # .group already allocated from the .call() above
s.delay = 1.0


# --- Nesting ---
# Trigger functions can call other trigger functions inside their body.
# inner only needs to be defined by the time outer.call() is first invoked, not before.
# If inner hasn't been built yet when outer's body runs, it is built at that point.

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
    inner.call()        # emits a spawn trigger to inner's group inside outer's chain
    inner.call(delay=1) # call it again later


# --- Parameterized variants: generator pattern ---
# @trigger_fn does not accept runtime parameters on the function itself.
# Wrap in a normal function to bake different values into separate, independent
# trigger functions. Each factory call produces its own group.
# Type checking on the factory's parameters works as normal.

def make_mover(target: int, amount: int):
    @trigger_fn
    def _fn():
        m = Move()
        m.target_id = target    # baked in at factory-call time, no placeholder IDs
        m.move_x = amount
        m.duration = 0.5
    return _fn

mover_a = make_mover(target=45, amount=100)     # owns its own group
mover_b = make_mover(target=67, amount=-100)    # completely independent group

with level_context(level):
    with autoappend():
        mover_a.call()
        mover_b.call(delay=1.0)
        mover_a.call(delay=2.0)  # calls the already-built mover_a again


# --- Properties ---

move_right.group    # IntEnum — the allocated group ID.
                    # For @trigger_fn(group=5): available immediately.
                    # For auto-allocated: lazily calls level.new.group() on first access.
                    # Raises if accessed without active level_context before allocation.

move_right.params   # list[int] | None — the remap allowlist.
                    # None means unrestricted (params not specified).

move_right.objects  # list[ObjectType] — every object built into this function,
                    # including objects in sub-groups created by wait().
                    # Empty list before first .call().
```
