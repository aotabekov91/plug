import os
import git
import shutil
from plug import Plug
from pip._internal import main as pipmain

class Picky(Plug):

    def __init__(
            self,
            *args,
            **kwargs,
            ):

        self.rtp={}
        self.repos=[]
        self.folder='~'
        self.install_picks=False
        self.base='https://github.com'
        super().__init__(
                *args, 
                **kwargs
                )

    def setup(self):

        super().setup()
        self.updateRTP()
        if self.install_picks:
            self.installPicks()

    def setSettings(self):

        super().setSettings()
        self.base=os.path.expanduser(
                self.base)
        self.folder=os.path.expanduser(
                self.folder) 
        self.app.createFolder(
                self.folder, 
                'picky_folder')
        if self.app.moder:
            self.app.moder.rtp=self.rtp

    def updateRTP(self):

        picks=self.config.get(
                'Picks', [])
        for data in picks:
            repo = data.get(
                    'pick', None)
            subdirs = data.get(
                    'subdir', [])
            if repo:
                n, p, f = self.getInfo(repo)
                self.rtp[n] = f
                for subdir in subdirs: 
                    url=f"{repo}/{subdir}"
                    n, p, f=self.getInfo(url)
                    self.rtp[n]=f

    def install(self):

        picks=self.config.get(
                'Picks', [])
        for data in picks:
            r = data.get('pick', None)
            if r: 
                self.installRepo(r)

    def getInfo(self, gid): 

        t=gid.split('/')
        h, n='', t[-1]
        if len(t)>2:
            h='/'.join(t[1:-1])
            h+='/'
        f=f"{self.folder}/{h}"
        p=f"{f}/{n}"
        return n, p, f

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
        r=os.path.join(
                path, 
                "requirements.txt"
                )
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
            p=os.path.join(
                    self.folder, name)
            repo = git.Repo(p)
            repo.remotes.origin.pull()

    def cleanupPicks(self):

        for d in os.listdir(self.folder):
            if not d in self.repos:
                p=os.path.join(
                        self.folder, d)
                shutil.rmtree(p)
