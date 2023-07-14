### Setup Blender as Python Module

https://wiki.blender.org/wiki/Building_Blender/Mac

- `brew install cmake svn`
- `mkdir ~/blender-git`
- `cd ~/blender-git`
- `git clone https://projects.blender.org/blender/blender.git`
- `cd blender`

Rendering of viewer nodes and previews in background mode was disabled in 2013 for speed optimization (see [here](https://archive.blender.org/wiki/index.php/Dev:Ref/Release_Notes/2.67/Compositing_Nodes/)).
However, you can easily enable it again by modifying 2 files of the blender sources and compiling blender yourself (as described [here](https://wiki.blender.org/index.php/Dev:Doc/Building_Blender)).

In the file source/blender/compositor/operations/COM_ViewerOperation.h, line ~58:

```c
bool isOutputOperation(bool /*rendering*/) const { if (G.background) return false; return isActiveViewerOutput();
```
should be changed to

```c
bool isOutputOperation(bool /*rendering*/) const {return isActiveViewerOutput(); }
```
and in file source/blender/compositor/operations/COM_PreviewOperation.h, line ~48:

```c
bool isOutputOperation(bool /*rendering*/) const { return !G.background; }
```
should be changed to

```c
bool isOutputOperation(bool /*rendering*/) const { return true; }
```
After these changes, the pixels array gets properly updated in background mode.
From [StackExchange](https://blender.stackexchange.com/a/81239/169566)

- `make update` (can use `-j`)
- `make bpy`
- `cd ../lib/darwin_arm64/python/lib/python3.10/site-packages/`

We're using [poetry](https://python-poetry.org/docs/) to manage dependencies.

For Python 3.10:
- `brew install pyenv`
- `pyenv install 3.10`
- `poetry env use ~/.pyenv/versions/3.10.12/python`
- `poetry install`
- `poetry shell`
- `cp -r ~/blender-git/lib/darwin_arm64/python/lib/python3.10/site-packages/bpy .venv/lib/python3.10/site-packages/`

Note that you need to have the project venv activated, that's what `poetry shell` does.
This means that if you exit your (tty) session, you'll have to re-run `poetry shell`.

To use `yapf` and `isort` you'll also need to install the dependencies in the `dev` group, by running `poetry install -E dev`

We're using the [yapf](https://github.com/google/yapf) formatter.
To format, if, e.g., you want to format all files in `src/`, go to `src/` and do `yapf -rpi --no-local-style --style "facebook" .`

We're using [isort](https://pycqa.github.io/isort/) to categorize our module imports; just `isort .`

To profile the code, a good starting point could be

```python
if __name__ == "__main__":
    import cProfile
    import pstats

    profiler = cProfile.Profile()
    profiler.enable()

    main()

    profiler.disable()
    profiler.dump_stats('main_stats.prof')

    stats = pstats.Stats('main_stats.prof')
    stats.sort_stats('cumulative').print_stats() # instead of 'cumulative', you can use 'time', etc.
```

The biggest contributor to performance right now (masked by the `bpy.ops_call` call in profiling) is the rendering itself.
The rendering parameter with the biggest impact in performance as it currently stands, is the [number of samples](https://docs.blender.org/manual/en/latest/render/eevee/render_settings/sampling.html) used by eevee.
