import os
import git
import shutil

class Picky:

    def __init__(self, picks, folder, base):

        self.rtp={}
        self.repos=[]
        self.picks=picks
        self.base=os.path.expanduser(base)
        self.folder=os.path.expanduser(folder)

    def installDependencies(self, name):
        pass

    def install(self):

        for data in self.picks:

            repo = data.get('pick', None)
            subdirs = data.get('subdir', [])

            if repo:

                name, folder = self.installDirect(repo)
                self.rtp[name] = folder

                for subdir in subdirs: 
                    url=f"{repo}/{subdir}"
                    name, path, folder=self.getInfo(url)
                    self.rtp[name]=folder

                self.installDirect(repo)

    def cleanup(self):

        for d in os.listdir(self.folder):
            if not d in self.repos:
                path=os.path.join(self.folder, d)
                shutil.rmtree(path)

    def update(self): 

        for name in self.repos:
            path=os.path.join(self.folder, name)
            print('Updating', path)
            repo = git.Repo(path)
            repo.remotes.origin.pull()

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

    def installDirect(self, gid):

        name, path, folder=self.getInfo(gid)

        self.rtp[name]=folder
        if not name in self.repos: 
            self.repos+=[name]

        if not os.path.exists(path):

            gpath=os.path.expanduser(gid)
            if os.path.exists(gpath):
                shutil.copy(gpath, path)
            else:
                url=f"{self.base}/{gid}"
                git.Repo.clone_from(url, path)

        return name, folder
