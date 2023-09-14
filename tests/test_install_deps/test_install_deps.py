import pytest
from pathlib import Path
from plug.utils.picky.install_deps import (
        getPoetries,
        updatePackages,
        installPackages,
        ) 

@pytest.fixture
def path():
    p=Path(__file__).parent
    return f'{p}/data/card', f'{p}/data/lura'

def test_getPoetries(path):

    pp, cp = path
    r = getPoetries(pp, cp)
    assert r is not None 

def test_updatePackages_not_none(path):

    pp, cp = path
    r = getPoetries(pp, cp)
    pp, cp = r
    p_dep=pp.package.dependency_group('main').dependencies
    c_dep=cp.package.dependency_group('main').dependencies
    updatePackages(pp, cp)
    for d in c_dep: assert d in p_dep

def test_installPackages(path):

    pp, cp = path
    pp, cp = getPoetries(pp, cp)
    updatePackages(pp, cp)
    installPackages(pp)
