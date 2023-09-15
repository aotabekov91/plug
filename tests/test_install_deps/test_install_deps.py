import os
import pytest
from pathlib import Path

from plug.utils.picky.install_deps import (
        installDeps,
        )

@pytest.fixture
def path():

    return Path(__file__).parent/'data/card'

def test_installDeps(path):

    assert os.path.exists(path)
    installDeps(path)
