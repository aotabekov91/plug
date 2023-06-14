from .base import BaseMode
from .helper import command

class InputMode(BaseMode):

    @command()
    def tabAction(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} Tab'

    @command(finishCheck=True)
    def escapeAction(self, request):
        return 'xdotool getactivewindow key Escape'
  
    @command(finishCheck=True)
    def enterAction(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} Enter'

    @command()
    def spaceAction(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} space'

    @command()
    def backspaceAction(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} BackSpace'

    @command()
    def interuptAction(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} ctrl+c'

    @command()
    def copyAction(self, request):
        return 'xdotool getactivewindow key ctrl+c'

    @command()
    def pasteAction(self, request):
        return 'xdotool getactivewindow key ctrl+v'

    @command()
    def downAction(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} Down'

    @command()
    def upAction(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} Up'

    @command()
    def leftAction(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} Left'

    @command()
    def rightAction(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} Right'

if __name__=='__main__':
    app=InputMode(port=33333)
    app.run()
