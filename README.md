SublistAlias
============

`SublistAlias` is a proxy object for Python list slices. You can use
`SublistAlias`es in places where normal lists can be used, but unlike modifying
a slice, modifying the `SublistAlias` will modify the original list, not a copy.

Check out [sublistalias.py](<sublistalias.py>) for docstring examples.
