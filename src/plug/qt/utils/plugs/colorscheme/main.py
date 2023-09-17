from plug.qt import Plug

class Colorscheme(Plug):

    def __init__(self, 
                 *args, 
                 update=True,
                 **kwargs):

        self.update=update
        super().__init__(*args, **kwargs)
        self.app.plugman.plugsLoaded.connect(
                self.addColorscheme)

    def addColorscheme(self, plugs):

        styler=plugs.get('Styler', None)
        file=self.files.get('colorscheme.css', None)
        if styler and file:

            style=styler.readColorscheme(file)
            styler.addColorscheme(
                    self.name, 
                    style,
                    self.update)
