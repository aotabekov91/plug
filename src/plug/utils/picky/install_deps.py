import os
from pathlib import Path
from cleo.io.null_io import NullIO
from poetry.factory import Factory
from poetry.utils.env import EnvManager
from poetry.installation.installer import Installer

def updatePackages(parent, child):

    group=child.package.dependency_group('main')
    for d in group.dependencies:
        parent.package.add_dependency(d)

def getPoetries(parent_path, child_path):

    n='pyproject.toml'
    c1=os.path.exists(os.path.join(parent_path, n))
    c2=os.path.exists(os.path.join(child_path, n))

    if not (c1 and c2): return

    child = Factory().create_poetry(Path(child_path))
    parent = Factory().create_poetry(Path(parent_path))
    return parent, child

def installPackages(parent):

    parent_env=EnvManager(parent).create_venv()
    installer = Installer(
        NullIO(),
        parent_env,
        parent.package,
        parent.locker,
        parent.pool,
        parent.config,
    )
    installer.update(True)
    installer.run()

def installDeps(parent_path, child_path):

    parent, child = getPoetries(parent_path,
                                child_path)
    updatePackages(parent, child)
    installPackages(parent)
