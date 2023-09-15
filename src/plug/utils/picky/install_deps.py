import os

def installDeps(ppath, cpath):

    r=os.path.join(cpath, "requirements.txt")
    if os.path.exists(r):
        os.popen(['pip', 'install', '-r', r])
