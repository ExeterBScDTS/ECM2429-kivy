# Asynchronous Web search

This lesson builds on the previous lesson to show how we might implement an asynchronous web API call.

Ensure you are familiar with the original program before studying this one.



Note that ```main.py``` has been changed significantly, but rather than re-writing ```searchtask.py``` a new class ```AsyncSearchTask``` is implemented in ```asyncsearchtask.py``` which inherits from ```SearchTask``` and replaces the use of the
```requests.get()``` call with ```aiohttp.ClientSession.get```

To learn more see

<https://docs.python.org/3/library/asyncio-task.html>

and

<https://docs.aiohttp.org/en/stable/>

## Does this solve all our problems?

The solution presented here is not perfect.  Can you see what some of the flaws might be?

## Packaging the app

```
python.exe -m PyInstaller --name lesson-07 lesson-07/code/main.py
```

Then edit lesson-07.spec as per <https://kivy.org/doc/stable/guide/packaging-windows.html>

Adding 

```
from kivy_deps import sdl2, glew
```

and changing the COLLECT section to

```
coll = COLLECT(exe,
               Tree('lesson-07\\code\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
                *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='lesson-07')
```

Check this works before moving on to create a **single file application**.