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

For Python 3.10:
- `brew install pyenv`
- `pyenv install 3.10`
- `poetry env use ~/.pyenv/versions/3.10.12/python`
- `poetry install`
- `poetry shell`
- `cp -r ~/blender-git/lib/darwin_arm64/python/lib/python3.10/site-packages/bpy .venv/lib/python3.10/site-packages/`
