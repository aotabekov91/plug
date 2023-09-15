import os

def installDeps(path):

    r=os.path.join(path, "requirements.txt")
    if os.path.exists(r):
        cmd=' '.join(['pip', 'install', '-r', r])
        os.popen(cmd)
