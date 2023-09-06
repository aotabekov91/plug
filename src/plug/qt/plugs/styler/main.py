import re
from collections import OrderedDict

from plug.qt import PlugObj
from plug.qt.utils import register

class Styler(PlugObj):

    def __init__(self, *args, **kwargs):

        self.current=None
        self.colorschemes={}
        self.m_colorscheme='default'

        super().__init__(*args, **kwargs)
        self.app.plugman.plugsLoaded.connect(
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
        self.setColorScheme(self.m_colorscheme)

        self.app.plugman.plugs.exec.addOptions(
                'colorscheme', 
                list(self.colorschemes.keys()))

    def updateColorScheme(self, style):

        default, css=self.colorschemes.get('default')
        tmp=default.copy()
        self.updateStyle(tmp, style)
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

            style=plug.tomls.get('style', {})
            self.updateStyle(default, style)

        style=self.app.tomls.get('style', {})
        self.updateStyle(default, style)
        css=self.dictToCSS(default)

        self.colorschemes['default']=(default, css)

    def addColorScheme(self, name, colorscheme):

        updated=self.updateColorScheme(
                colorscheme)
        css=self.dictToCSS(updated)
        self.colorschemes[name]=(updated, css)

        self.app.plugman.plugs.exec.addOptions(
                'colorscheme', 
                list(self.colorschemes.keys()))

    def reloadColorScheme(self):

        if self.current!=self.m_colorscheme:
            self.setColorScheme(self.m_colorscheme)

    @register(modes=['exec'])
    def setColorScheme(self, name, test=None):
        
        style=self.colorschemes.get(name, None)

        if style:
            cdict, css=style
            self.current=name
            self.m_colorscheme=name
            self.app.setStyleSheet(css)
        else:
            self.current=None
