# Context managers

The context managers provided are for automatically applying changes made to newly made objects.
They help a lot with eliminating a lot of duplicate code when you make many objects that you need configured with similar properties. 
Since the implementation is based on ContextVars, it is thread-safe by default.

You may find all the context manager implementations under `gmdbuilder/context.py`.

## Usage

Note that some of them will require `level_context` to be scoped first, since certain utils like `autoappend` need direct level access.

Like any other context managers in Python, you use them like so:

```python

from gmdbuilder import level_context, autoappend, targets

with level_context(level):
    with autoappend(), targets(target=4,target_2=5):
        # All auto appended, targets 4 and targets 5 as a secondary target
        # autoappend() is called before targets()
        m = new_obj(901)
        m2 = Move()
        a = from_object_string("1,1611,2,50,3,45;", obj_type=CountType)
```

Note from the snippet that you can combine context managers in one line to avoid extra scoping. 
A lesser known Python feature.

::: tip
If you don't need to edit multiple levels, scope using `with level_context(level):` just once at your `if __name__ == "__main__":` entry point. 
This helps configure context managers like `autoappend` for your entire project's runtime.
:::

### Order

The actions applied by the context managers are done in order of least-to-most nested.
```python
from gmdbuilder import level_context, groups, autoappend

with level_context(level):
    with groups(10):
        m1 = new_obj(901) # has group 10
        with autoappend(), groups(67):
            m2 = new_obj(1611) # has group 67 and 10, auto appends
        m3 = new_obj(1268) # has group 10
```

Example to reduce repetitive editing:

```python
from gmdbuilder import transform

def set_spawn_multi(obj: ObjectType):
   obj["a62"] = True # SPAWN_TRIGGER
   obj["a87"] = True # MULTI_TRIGGER
   obj["a11"] = False # TOUCH_TRIGGER

with transform(set_spawn_multi):
    # The two new move triggers are immediately configured
    a = Move()
    b = Move()
```

## Context Manager List

| Name | Description
|---|--
| level_context | Provides given the `level` instance to other context managers. 
| autoappend | Requires `level_context`. Auto appends new objects. 
| transform | Applies a given function to mutate new objects. 
| set_prop | Applies a given key and value to new objects. 
| groups | Adds one or more group IDs to new objects.
| target | Set target property `a51` and/or target property `a71` to new objects.

[See Implementation](./index)