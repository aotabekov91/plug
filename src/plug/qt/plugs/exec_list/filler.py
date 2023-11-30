import os

class Filler:

    def getPaths(self, path):

        t=path.rsplit('/', 1)
        if len(t)==2:
            p, c = t[0]+'/', t[1] 
        else:
            p, c = '.', t[0] 
        clist=[]
        for i in os.listdir(p):
            if i[:len(c)]==c:
                if p!='.':
                    i=os.path.join(p, i)
                clist+=[i.replace(' ', '\ ')]
        return clist
