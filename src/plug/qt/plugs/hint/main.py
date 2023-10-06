from plug.qt import Plug

from gizmo.widget import HintLabel

class Hint(Plug):

    def __init__(self, 
                 app, 
                 name='hint',
                 listen_leader='<c-h>',
                 **kwargs,
                 ):

        super(Hint, self).__init__(
                app=app, 
                name=name, 
                listen_leader=listen_leader,
                **kwargs,
                )

        self.ear.keyPressed.connect(
                self.on_keysPressed)

    def listen(self):

        super().listen()
        self.hint()

    def delisten(self):

        super().delisten()
        self.dehint()

    def hint(self):

        def getNodes(node, coor):

            if node.widget:
                coor+=[node]
            for leaf in node.leaves:
                getNodes(leaf, coor)
            return coor

        display=self.app.display
        root=display.m_layout.root
        nodes=getNodes(root, [])

        self.labels={}

        for i, n in enumerate(nodes):
            self.labels[i+1]=n
            l=HintLabel(str(i+1), parent=display)
            l.setGeometry(n.x, n.y, n.w, n.h)
            l.setStyleSheet('color: green;')
            n.label=l
            l.show()

    def dehint(self):

        for i, n in self.labels.items():
            n.label.hide()
            n.label.setParent(None)
            n.label=None

    def on_keysPressed(self, digit, key):

        node=self.labels.get(digit, None)
        if node:
            print(node.widget)
            self.app.display.focusView(
                    node.widget)
        self.delistenWanted.emit()
