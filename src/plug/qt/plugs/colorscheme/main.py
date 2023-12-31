from plug.qt import Plug

class Colorscheme(Plug):

    def __init__(self, 
                 *args, 
                 update=True,
                 **kwargs):

        self.update=update
        super().__init__(*args, **kwargs)
        self.app.moder.plugsLoaded.connect(
                self.addColorscheme)

    def addColorscheme(self, plugs):

        styler=plugs.get(
                'styler', None)
        file=self.files.get(
                'colorscheme.css', None)
        if styler and file:
            style=styler.read(file)
            styler.addColorscheme(
                    self.name, 
                    style,
                    self.update)
