import os
import threading
import subprocess

def installDeps(path):

    r=os.path.join(path, "requirements.txt")
    if os.path.exists(r):
        cmd=' '.join(['pip', 'install', '-r', r])
        thread=runCMD(cmd)
        thread.join()

def runCMD(cmd):

    def run(): subprocess.call(cmd)

    thread=threading.Thread(target=run)
    thread.start()
    return thread
