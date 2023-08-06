import zmq
import pytest
from plug import Plug

@pytest.fixture
def plug(): return Plug(listen_port=False)

@pytest.fixture
def psocket(): 

    port=33331
    socket=zmq.Context().socket(zmq.REP)
    socket.connect(f'tcp://localhost:{port}')
    return socket

def test_app_initiated(plug): 
    assert plug.__class__.__name__=='Plug'

def test_intent_and_entity_properties(plug):

    c1=hasattr(plug, 'intents')
    c2=hasattr(plug, 'entities')
    assert c1 and c2

def test_no_parent_port_working(plug):

    plug.parent_port=33333
    respond=plug.registerByParent()
    assert respond['status']=='nok'
