import os
import git
import shutil
from pip._internal import main as pipmain

from plug.utils.miscel import dotdict

class Picky:

    def __init__(
            self, app, moder):

        self.app=app
        self.repos=[]
        self.folder='~'
        self.moder=moder
        self.base='https://github.com'
        super().__init__()
        self.setup()

    def setup(self):

        self.config=self.app.config.get(
                'Picky', {})
        self.setSettings()
        self.updateRTP()

    def setSettings(self):

        s=self.config.get('Settings', {})
        for k, v in s.items():
            setattr(self, k, v)
        self.base=os.path.expanduser(
                self.base)
        self.folder=os.path.expanduser(
                self.folder) 
        self.app.createFolder(
                self.folder, 'picky_folder')

    def updateRTP(self):

        rtp={}
        picks=self.config.get(
                'Picks', [])
        for data in picks:
            repo = data.get('pick', None)
            subdirs = data.get('subdir', [])
            if repo:
                n, p, f = self.getInfo(repo)
                rtp[n] = f
                for subdir in subdirs: 
                    url=f"{repo}/{subdir}"
                    n, p, f=self.getInfo(url)
                    rtp[n]=f
        self.moder.rtp.update(rtp)

    def install(self):

        picks=self.config.get(
                'Picks', [])
        for data in picks:
            r = data.get('pick', None)
            if r: self.installRepo(r)

    def getInfo(self, gid): 

        t=gid.split('/')
        h, n='', t[-1]
        if len(t)>2:
            h='/'.join(t[1:-1])
            h+='/'
        folder=f"{self.folder}/{h}"
        path=f"{folder}/{n}"
        return n, path, folder

    def installRepo(self, repo):

        n, p, f=self.getInfo(repo)
        self.moder.rtp[n]=f
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
        for n, p in self.moder.rtp.items():
            p=os.path.join(p, n)
            for r in self.getReqs(p):
                if not r in reqs:
                    reqs+=[r]
        self.installReqs(reqs)

    def getReqs(self, path):

        reqs=[]
        r=os.path.join(
                path, "requirements.txt")
        if os.path.exists(r):
            with open(r, 'r') as f:
                for i in f.readlines():
                    reqs+=[i.strip('\n')]
        return set(reqs)

    def installReqs(self, reqs):

        for r in reqs:
            pipmain(['install', r])

    def installPicks(self): 

        self.install()
        self.installRequirements()

    def updatePicks(self): 

        for name in self.repos:
            path=os.path.join(self.folder, name)
            repo = git.Repo(path)
            repo.remotes.origin.pull()

    def cleanupPicks(self):

        for d in os.listdir(self.folder):
            if not d in self.repos:
                path=os.path.join(self.folder, d)
                shutil.rmtree(path)
