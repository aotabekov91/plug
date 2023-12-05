from PyQt5.QtGui import QStandardItem
from inspect import signature, Parameter

from plug.qt import Plug
from gizmo.utils import tag
from gizmo.vimo.model import SModel
from plug.plugs.parser import Parser

from .filler import Filler
from .widget import ExecList

class Exec(Plug):

    name='exec'
    listen_leader='<c-e>'
    position={'ui': 'overlay'}

    def setup(self):

        super().setup()
        self.setupUI()
        self.params={}
        self.options={}
        self.functions={}
        self.parameters={}
        self.setupParser()
        self.filler=Filler()
        self.bar=self.app.ui.bar
        self.app.earman.objectAdded.connect(
                self.saveFuncs)
        
    @tag('<tab>', modes=['exec|ExecList'])
    def fill(self):

        item=self.ui.currentItem()
        if item:
            text=item.itemData
            self.app.ui.bar.edit.setText(text)

    @tag('<c-m>', modes=['exec|ExecList'])
    def fillex(self):

        self.fill()
        self.execute()

    @tag(['<return>', '<enter>'], modes=['exec|ExecList'])
    def execute(self): 

        t=self.app.ui.bar.edit.text()
        try:
            c, _ = self.parser.parse(t)
        except:
            c = None
        if c and c.exec:
            args=vars(c)
            cmd=args.pop('exec')
            f=self.functions.get(cmd)
            f(**args)
        self.octivate()

    def setupUI(self):

        self.ui=ExecList()
        self.model=SModel()
        self.ui.bar=self.app.ui.bar
        self.ui.setModel(self.model)
        self.app.uiman.setupUI(
                self, self.ui)
        self.app.handler.viewAdded.emit(
                self.ui)

    def setupParser(self):

        self.parser=Parser()
        s=self.parser.addSubParser(
                dest='exec', required=False)
        self.subparser=s

    def setArgOptions(
            self, cname, aname, alist):

        if not cname in self.options:
            self.options[cname]={}
        self.options[cname][aname]=alist

    def saveFuncs(self, plugs):

        ms=self.app.earman.m_methods
        exec_funcs=ms.get('exec', [])
        any_funcs=ms.get('any', [])
        funcs=exec_funcs+any_funcs
        for m in funcs: 
            n=m.__name__
            if n in self.functions: 
                continue
            self.functions[n]=m
            prmts=signature(m).parameters
            p=self.subparser.add_parser(n)
            if not n in self.parameters:
                self.params[n]=[]
                self.parameters[n]=[]
            for i, v in prmts.items():
                d=None
                if i=='kwargs':
                    d={}
                elif v.default!=Parameter.empty:
                    d=v.default
                if d is None:
                    self.params[n]+=[i]
                    p.add_argument(i)
                else:
                    p.add_argument(i, default=d)
                self.parameters[n]+=[i]

    def activate(self):

        super().activate()
        self.app.handler.activateView(
                self.ui)
        self.app.handler.setView(self.ui)
        self.ui.setFocus()
        self.bar.edit.textChanged.connect(
                self.updateUI)
        self.activateBar()
        self.app.earman.setPassive(
                True, ['exec'])
        self.updateUI()

    def octivate(self):

        super().octivate()
        self.octivateBar()
        self.bar.edit.textChanged.disconnect(
                self.updateUI)
        self.app.earman.setPassive()

    def octivateBar(self):

        self.bar.bottom.hide()
        self.bar.edit.clear()

    def activateBar(self):

        self.bar.bottom.show()
        self.bar.show()
        self.bar.edit.setFocus()

    def updateUI(self, keys=None):

        self.model.clear()
        self.ui.updatePosition()
        m = self.suggest()
        if m:
            for i, t in m.items():
                s=QStandardItem(i)
                s.itemData=t
                self.model.appendRow(s)
            idx=self.ui.getRowIndex(0)
            self.ui.setCurrentIndex(idx)
            self.ui.updatePosition()

    def suggest(self): 

        def match(t, alist=[], pref=''):

            if len(alist)<2:
                return alist
            p = []
            for i in alist:
                n=f'{pref}{i}'
                if n.startswith(t): 
                    p+=[n]
            return p

        t=self.app.ui.bar.edit.text()
        m=[]
        pref=''
        alist=[]
        # replace=True
        c=t.endswith(' ')
        s=self.parser.split(t)
        alts={}
        if len(s)==0: 
            k=self.functions.keys()
            return {i:i for i in k}
        cmd=s[0]
        opts=self.options.get(cmd, {})
        args=self.parameters.get(s[0], [])
        if not c and len(s)==1:
            alist=self.functions.keys()
        elif s[-1].startswith('--'):
            if not c:
                pref='--'
                alist=args
        elif len(s)>2 and s[-2].startswith('--'):
            arg=s[-2][2:]
            alist=opts.get(arg, [])
            if type(alist)==str:
                data={}
                if not c: data[arg]=s[-1]
                alist=self.filler.get(
                        kind=alist, 
                        data={arg: s[-1]})
        if not alist :
            d=0
            idx=-1
            for i in s:
                if not i.startswith('--'):
                    idx+=(1+d)
                    d=0
                else:
                    d=-1
            cmd=s[0]
            p=self.params.get(cmd, None)
            if not c: idx-=1
            if p and idx<len(p):
                arg=p[idx]
                alist=opts.get(arg, [])
                if type(alist)==str:
                    data={}
                    if not c: data[arg]=s[-1]
                    alist=self.filler.get(
                            kind=alist, 
                            data=data)
                    # replace=False
        if alist:
            mm = match(s[-1], alist, pref)
            ss=s.copy()
            for m in mm:
                # if replace:
                #     s[-1]=m[0]
                #     # s+=[' ']
                #     text=' '.join(s)
                # else:
                if c:
                    ss+=m
                else:
                    ss[-1]=m
                text=' '.join(ss)
                alts[m]=text
        return alts 
