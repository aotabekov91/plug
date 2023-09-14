import os
import pytest
from plug.utils.picky.install_deps import (
        getPoetries
        ) 

@pytest.fixture
def path():
    parent=os.path.expanduser('~/code/lura')
    child=os.path.expanduser('~/code/lura_plugins/src/plugs/card')
    return parent, child


def test_getPoetries(path):
    pp, cp = path
    p, c = getPoetries(pp, cp)






