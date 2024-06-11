#########################
Rack, another shelve-like
#########################


Rack contains `PersistentSet` and `PersistentDict`
classes that can be used to store data using set/dict semantics,
while having contents persisted to mass storage.

This library can be used when you want to use sets or mappings that
may be too big to fit in RAM, or you want them to be persisted to disk,
either online (as they're used) or once (to load/save data).

It uses LMDB or SQLite3 as underlying engine:

- LMDB is a tiny in-process "NoSQL" database which is very fast.

- SQLite3 is a small in-process SQL database which stores data in
  single files, with a well-defined on-disk layout, and is rather
  space-efficient.

Contents are serialized from / deserialized to Python native objects
on access, so the structures are obviously slower than in-memory
counterparts.


Usage
#####

Use `rack.set*.PersistentSet` as you would use a `set`,
and `rack.dict*.PersistentDict` as you would use a `dict`,
except that:

- On construction:

  - They need to take a `name` argument indicating the
    (prefix to the) location of the underlying LMDB database.

  - For LMDB, they can take a `hash` argument if you want to specify
    a non-default hasher (default is SHA256).

  - They can take a `serdes` argument which you can use to specify
    a non-default serializer/deserializer (default is Python's
    marshal).

- On use:

  - They must be used with a context manager, which is required
    in order to properly manage the lifetime of the database open/close,
    as `__init__` / `__del__` would not be sufficient due to the
    garbage collected nature of Python.

  - Operations that create a new container (eg. union, copy),
    take an optional name parameter, which allows to specify the
    location of the new database.

If you know you store elements of limited size (less than LMDB max key
size), you can use `rack.set_small.PersistentSet`, which is ~2x faster
than the non-small one due to one less indirection. If keys are too
big, `lmdb.BadValsizeError` exceptions will occur.

