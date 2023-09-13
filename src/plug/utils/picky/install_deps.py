from io import StringIO
from pathlib import Path
from cleo.io.null_io import NullIO
from poetry.factory import Factory
from poetry.utils.env import EnvManager
from poetry.installation.installer import Installer

def installDeps(parent_path, child_path):

    child = Factory().create_poetry(Path(child_path))
    parent = Factory().create_poetry(Path(parent_path))
    parent_env=EnvManager(parent).create_venv()

    group=child.package.dependency_group('main')

    for d in group.dependencies:
        parent.package.add_dependency(d)

    installer = Installer(
        StringIO(),
        parent_env,
        parent.package,
        parent.locker,
        parent.pool,
        parent.config,
    )

    installer.update(True)
    installer.run()
