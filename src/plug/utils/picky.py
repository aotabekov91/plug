import os
import git
import shutil
from pip._internal import main as pipmain

class Picky:

    def __init__(self, picks, folder, base):

        self.rtp={}
        self.repos=[]
        self.picks=picks
        self.base=os.path.expanduser(base)
        self.folder=os.path.expanduser(folder)
        self.updateRunTimePaths()

    def updateRunTimePaths(self):

        for data in self.picks:
            repo = data.get('pick', None)
            subdirs = data.get('subdir', [])
            if repo:
                n, p, f = self.getInfo(repo)
                self.rtp[n] = f
                for subdir in subdirs: 
                    url=f"{repo}/{subdir}"
                    n, p, f=self.getInfo(url)
                    self.rtp[n]=f

    def install(self):

        for data in self.picks:
            r = data.get('pick', None)
            if r: self.installRepo(r)

    def update(self): 

        for name in self.repos:
            path=os.path.join(self.folder, name)
            print('Updating', path)
            repo = git.Repo(path)
            repo.remotes.origin.pull()

    def cleanup(self):

        for d in os.listdir(self.folder):
            if not d in self.repos:
                path=os.path.join(self.folder, d)
                shutil.rmtree(path)

    def getInfo(self, gid): 

        name_space=gid.split('/')
        name=name_space[-1]
        holder=''
        if len(name_space)>2:
            holder='/'.join(name_space[1:-1])
            holder+='/'
        folder=f"{self.folder}/{holder}"
        path=f"{folder}/{name}"
        return name, path, folder

    def installRepo(self, repo):

        n, p, f=self.getInfo(repo)
        self.rtp[n]=f
        if not n in self.repos: 
            self.repos+=[n]
        if not os.path.exists(p):
            gpath=os.path.expanduser(repo)
            if os.path.exists(gpath):
                shutil.copy(gpath, p)
            else:
                url=f"{self.base}/{repo}"
                git.Repo.clone_from(url, p)
        return n, f

    def installRequirements(self):

        reqs=[]
        for n, p in self.rtp.items():
            p=os.path.join(p, n)
            for r in self.getReqs(p):
                if not r in reqs:
                    reqs+=[r]
        self.installReqs(reqs)

    def getReqs(self, path):

        reqs=[]
        r=os.path.join(path, "requirements.txt")
        if os.path.exists(r):
            with open(r, 'r') as f:
                for i in f.readlines():
                    reqs+=[i.strip('\n')]
        return set(reqs)

    def installReqs(self, reqs):

        for r in reqs:
            pipmain(['install', r])
