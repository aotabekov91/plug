import os
from pathlib import Path
from poetry.factory import Factory
from poetry.utils.env import EnvManager
from poetry.installation.installer import Installer

from clikit.io.console_io import ConsoleIO
from cleo.io.io import IO

def installDeps(self, ppath, cpath):

    cp = Factory().create_poetry(Path(cpath))
    pp = Factory().create_poetry(Path(ppath))

    io = ConsoleIO()
    penv=EnvManager(pp).create_venv()
    # io = ConsoleIO()

    installer = Installer(
        io,
        penv,
        pp.package,
        pp.locker,
        pp.pool,
        pp.config,
    )

    installer.update(True)
    installer.run()


project_path='.'
poetry = Factory().create_poetry(Path(project_path))

# io = ConsoleIO()
io = NullIO()
installer = Installer(
    io,
    EnvManager(poetry).create_venv(io),
    poetry.package,
    poetry.locker,
    poetry.pool,
    poetry.config,
)
installer.update(True)
installer.run()
