import os

def installDeps(ppath, cpath):

    r=os.path.join(cpath, "requirements.txt")
    print(r)
    if os.path.exists(r):
        with open(r, 'r') as f:
            for l in f.readlines():
                req=l.strip('\n')
                os.popen(['pip', 'install', '-r', req])
