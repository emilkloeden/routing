# routing-example

`main.py` dynamically creates a dictionary of paths relative to a "routes" subdirectory to a dictionary of HTTP methods to functions named "respond" in a python file named {method}.py.

For example, in the folder structure included in this repo

```
routes\
 - get.py
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
    '/': {
        'get': <function respond at 0x00000193672DA560>
    },
    '/users/{id}': {
        'get': <function respond at 0x00000193672DA710>,
        'post': <function respond at 0x00000193672DA830>
    },
    '/users/{id}/job': {
        'get': <function respond at 0x00000193672DA9E0>,
        'post': <function respond at 0x00000193672DAB90>
    }
}
```

In other words, it serves as a step towards developing a folder-based request router.
