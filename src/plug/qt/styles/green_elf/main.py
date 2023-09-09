from plug.qt.plugs import Colorscheme

class GreenElf(Colorscheme): 

    def __init__(self,
                 *args,
                 update=False,
                 **kwargs):

        super().__init__(*args, 
                         update=update, 
                         **kwargs)
