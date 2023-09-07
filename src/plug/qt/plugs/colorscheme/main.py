from plug.qt import PlugObj

class Colorscheme(PlugObj):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.app.plugman.plugsLoaded.connect(
                self.addColorscheme)

    def addColorscheme(self):

        styler=self.app.plugman.plugs.get(
                'Styler', None)
        cs=self.tomls.get('colorscheme', None)
        if cs: 
            styler.addColorscheme(self.name, cs)
            styler.reloadColorscheme()

