import os

class Filler:

    def get(self, kind, data):

        if kind:
            n=f'get{kind.title()}'
            f=getattr(self, n, None)
            if f: return f(**data)
        return []

    def getPath(self, path=None):

        path = path or os.path.abspath('.')
        t=path.rsplit('/', 1)
        if len(t)==2:
            p, c = t[0]+'/', t[1] 
        else:
            p, c = '.', t[0] 
        clist=[]
        try:
            for i in os.listdir(p):
                if i[:len(c)]==c:
                    if p!='.':
                        i=os.path.join(p, i)
                    clist+=[i.replace(' ', '\ ')]
        except:
            pass
        finally:
            return clist
