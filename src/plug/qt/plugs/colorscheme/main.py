from plug.qt import PlugObj

class ColorScheme(PlugObj):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.app.plugman.plugsLoaded.connect(
                self.addColorScheme)

    def addColorScheme(self):

        styler=self.app.plugman.plugs.get(
                'Styler', None)
        cs=self.tomls.get('colorscheme', None)
        if cs: 
            styler.addColorScheme(self.name, cs)
            styler.reloadColorScheme()
