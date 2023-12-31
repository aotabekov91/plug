import re
from collections import OrderedDict

from plug.qt import Plug
from gizmo.utils import tag

class Styler(Plug):

    styles={}
    current=None
    style='default'

    def setup(self):

        super().setup()
        self.app.moder.plugsLoaded.connect(
                self.on_plugsLoaded)

    def cssToDict(self, css):

        css=css.strip()
        css=re.sub(r'[\n\t]', ' ', css)
        css=re.sub('}', '}__::__', css)
        pattern=r'([^{]*){([^}]*)}'
        s={}
        tmp=css.split('__::__')
        for t in tmp:
            if t: 
                t=t.strip()
                m=re.match(pattern, t)
                if m:
                    name=m.group(1).strip()
                    inside=m.group(2).strip()
                    m={}
                    for i in inside.split(';'):
                        if i:
                            i=i.strip()
                            j=i.split(':', 1)
                            m[j[0].strip()]=j[1].strip()
                    s[name]=m
        return s

    def dictToCSS(self, style): 

        parts=[]
        for k, v in style.items():
            inside=[]
            for i, j in v.items():
                inside+=[f' {i}: {j}']
            inside='; '.join(inside)+ '; }'
            parts+=[k+' {' +f' {inside} ']
        css=' '.join(parts)
        return css

    def on_plugsLoaded(self, plugs):

        self.setDefault(plugs)
        self.colorscheme(self.style)
        self.addToRunList(plugs)

    def updateColorscheme(self, cs):

        default, css=self.styles.get('default')
        tmp=default.copy()
        self.updateStyle(tmp, cs)
        return tmp

    def updateStyle(self, base, append):

        for n, a in append.items():
            v=base.pop(n, {})
            v.update(a)
            base[n]=v

    def setDefault(self, plugs):

        default=OrderedDict()
        for name, plug in plugs.items():
            if hasattr(plug, 'ui'):
                style=plug.ui.styleSheet()
                if style: 
                    style=self.cssToDict(style)
                    self.updateStyle(default, style)

            file=plug.files.get('style.css', None)
            if file:
                style=self.read(file)
                self.updateStyle(default, style)

        file=self.app.files.get('style.css', None)
        if file:
            style=self.read(file)
            self.updateStyle(default, style)
        css=self.dictToCSS(default)
        self.styles['default']=(default, css)

    def read(self, path):

        with open(path, 'r') as y:
            lines=' '.join(y.readlines())
            css=re.sub(r'[\n\t]', ' ', lines)
            return self.cssToDict(css)

    def addColorscheme(
            self, name, cs, update=True):

        if update:
            cs=self.updateColorscheme(cs)
        css=self.dictToCSS(cs)
        self.styles[name]=(cs, css)
        self.reloadColorscheme()
        self.addToRunList()

    def addToRunList(self, plugs=None):

        plugs = plugs or self.app.moder.plugs
        p=getattr(plugs, 'exec', None)
        if p:
            p.setArgOptions(
                    'colorscheme', 
                    'name', 
                    self.styles.keys())

    def reloadColorscheme(self):

        if self.current!=self.style:
            self.colorscheme(self.style)

    @tag(modes=['exec'])
    def colorscheme(self, name=None):
        
        style=self.styles.get(name, None)
        if style:
            cdict, css=style
            self.current=self.style=name
            self.app.qapp.setStyleSheet(css)
        else:
            self.current=None
