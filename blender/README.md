### Setup Blender as Python Module

https://wiki.blender.org/wiki/Building_Blender/Mac

- `brew install cmake svn`
- `mkdir ~/blender-git`
- `cd ~/blender-git`
- `git clone https://projects.blender.org/blender/blender.git`
- `cd blender`
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
