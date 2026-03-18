# Trigger Wrappers

To help with trigger editing, `gmdbuilder` provides object wrapper classes.
The classes provide clean interfaces for property access, as well as helper methods. They can be found in `gmdbuilder/classes`.

All wrapper classes contain a `.obj` property in which stores the actual underlying object. 
Although you can wrap existing objects, it's constructor may help. The field properties support static type checking for read/write. 


::: info
Many of the wrappers lack any real functionality other than property field editing. Many triggers are also missing. 
If you find any wrapper methods to be good official additions, please contact me, open an issue or send a PR.
:::

## Example

```python
from gmdbuilder.classes import Move, Count

# Typical way
a = new_obj(obj_id.Trigger.MOVE)
a[obj_prop.X] = 0
a[obj_prop.Y] = 0
a[obj_prop.Trigger.Move.TARGET_ID] = 10

# With wrappers
b = Move.wrap(a)
b.reset_transform()
b.move_by(dx=30, dy=60, t=0.5)
b.spawn_trigger = True

c = Count() # makes a new Count object
c.count = 5
c.target_id = 14
c.item_id = 10

level.objects.append(b.obj) # same reference as 'a'
level.objects.append(c.obj)
```

## See [Wrapper Classes](./classes) Reference page.