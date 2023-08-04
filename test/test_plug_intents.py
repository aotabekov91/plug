import pytest
from plug import Plug

@pytest.fixture
def app(): return Plug(listen_port=False)

def test_app_initiated(app): 
    assert app.__class__.__name__=='Plug'

def test_intent_and_entity_properties(app):

    for name, plug in app.plugs.plugs.items():
        c1=hasattr(plug, 'intents')
        c2=hasattr(plug, 'entities')
        assert c1 and c2
