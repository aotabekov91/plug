from clikit.io.console_io import ConsoleIO
from poetry.factory import Factory
from poetry.installation.installer import Installer
from poetry.utils.env import EnvManager

poetry = Factory().create_poetry(Path(project_path))
io = ConsoleIO()
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
