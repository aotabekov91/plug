
from cleo.io.null_io import NullIO
from poetry.core.packages.dependency import Dependency
from poetry.core.packages.project_package import ProjectPackage

from poetry.config.config import Config
from poetry.installation.installer import Installer
from poetry.packages.locker import Locker
from poetry.repositories.installed_repository import InstalledRepository

# We build Poetry dependencies from the requirements
package = ProjectPackage("__root__", "0.0.0")
package.python_versions = ".".join(str(v) for v in self._env.version_info[:3])

for requirement in requirements:
    dependency = Dependency.create_from_pep_508(requirement)
    package.add_dependency(dependency)

installer = Installer(
    NullIO(),
    self._env,
    package,
    Locker(self._env.path.joinpath("poetry.lock"), {}),
    self._pool,
    Config.create(),
    InstalledRepository.load(self._env),
)
installer.update(True)
installer.run()

