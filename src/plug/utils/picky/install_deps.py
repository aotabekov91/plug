import os
from pip._internal import main as pipmain

def installDeps(path):

    reqs=getReqs(path)
    installReqs(reqs)

def getReqs(path):

    r=os.path.join(path, "requirements.txt")
    reqs=[]
    if os.path.exists(r):
        with open(r, 'r') as f:
            for i in f.readlines():
                reqs+=[i.strip('\n')]
    return reqs

def installReqs(reqs):

    for req in reqs:
        pipmain(['install', req])
