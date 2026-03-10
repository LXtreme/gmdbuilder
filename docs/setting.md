# Validation Settings

The `setting` class holds global flags that control which checks are active.

```python
from gmdbuilder import setting
```

All flags are global attributes — set them directly:
```python
setting.property_allowed_check = False
```


::: tip
`property_allowed_check` and `property_type_check` are the two checks you're most likely to touch if you need flexibility.
:::

Flag list:

| Setting | Status |
|---|---|
| `property_allowed_check` | Complete |
| `property_type_check`  | Complete |
| `target_exists_check`  | Incomplete |
| `spawn_limit_check`  | Not Implemented |
| `solid_target_check`  | Not Implemented |
| `group_parent_check`  | Not Implemented |

## Flags

### `property_allowed_check` (default: `True`)

Raises if you assign a key that isn't valid for that object's ID. For example, assigning a Move trigger property to a Spawn trigger:

```python
obj = new_obj(obj_id.Trigger.SPAWN)
obj[obj_prop.Trigger.Move.DURATION] = 1.0  # raises ValueError
```

### `property_type_check` (default: `True`)

Raises if the value assigned to a property is the wrong Python type, or a numeric value is outside GD's accepted range:

```python
obj[obj_prop.Trigger.Move.DURATION] = "fast"  # raises ValueError: wrong value type
obj[obj_prop.Trigger.Move.TARGET_ID] = 99999  # raises ValueError: out of range
```

### `target_exists_check` (default: `False`)

Warns if a trigger targets a group ID that no object in the level belongs to. Useful for catching dead references before exporting:

```python
setting.target_exists_check = True
```

::: info
This check does not yet cover all trigger types (e.g. Pulse's color ID targets). It will warn conservatively rather than silently miss cases.
:::

### `solid_target_check` (default: `False`)

Intended to warn when a visual trigger (e.g. Move, Rotate) targets a group that only contains other triggers rather than visible objects. Not yet implemented.

### `spawn_limit_check` (default: `False`)

Intended to detect spawn loop situations in trigger execution chains. Not yet implemented.

### `group_parent_check` (default: `False`)

Intended to detect when more than one object claims to be the parent of the same group ID. Not yet implemented.
