# routing-example

`main.py` dynamically creates a dictionary of paths relative to a "routes" subdirectory to a dictionary of HTTP methods to functions named "respond" in a python file named {method}.py.

For example, in the folder structure included in this repo

```
routes\
 - users\
   - {id}\
     - get.py
     - job\
       - get.py
       - post.py
     - post.py
```

a dictionary would be created with contents:

```py
{
   'users/{id}': {
        'get': <function respond at 0x000001C9E3B7A680>,
        'post': <function respond at 0x000001C9E3B7A7A0>
    },
    'users/{id}/job': {
        'get': <function respond at 0x000001C9E3B7A950>,
        'post': <function respond at 0x000001C9E3B7AB00>
    }
}
```

In other words, it serves as a step towards developing a folder-based request router.
