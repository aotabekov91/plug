import os
import pytest
from pathlib import Path

from plug.utils.picky.install_deps import (
        installDeps,
        # getReqs,
        installReqs,
        )

from pip._internal import main as pipmain

@pytest.skip
def test_new():

    assert pipmain(['install', 'ankipulator @ git+https://github.com/aotabekov91/ankipulator@main'])

@pytest.fixture
def path():

    return Path(__file__).parent/'data/card'

def test_getReqs(path):

    assert os.path.exists(path)
    # assert getReqs(path)
