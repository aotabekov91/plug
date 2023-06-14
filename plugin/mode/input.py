from .mode import Mode
from .utils import command

class InputMode(Mode):

    @command()
    def tab(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} Tab'

    @command(finishCheck=True)
    def escape(self, request):
        return 'xdotool getactivewindow key Escape'
  
    @command(finishCheck=True)
    def enter(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} Enter'

    @command()
    def space(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} space'

    @command()
    def backspace(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} BackSpace'

    @command()
    def interupt(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} ctrl+c'

    @command()
    def copy(self, request):
        return 'xdotool getactivewindow key ctrl+c'

    @command()
    def paste(self, request):
        return 'xdotool getactivewindow key ctrl+v'

    @command()
    def down(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} Down'

    @command()
    def up(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} Up'

    @command()
    def left(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} Left'

    @command()
    def right(self, request):
        return 'xdotool getactivewindow key --repeat {repeat} Right'

if __name__=='__main__':
    app=InputMode(port=33333)
    app.run()
