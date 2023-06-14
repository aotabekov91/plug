from PyQt5.QtWebEngineWidgets import *

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Browser(QWebEngineView):
    def __init__(self):
        super().__init__()

        self.html = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>Title</title>
                <meta charset="utf-8" />
            </head>
            <body>
                <p>{}</p>
            </body>
        </html>
        """

    def loadHtml(self, html):
        self.page().setHtml(html)#, baseUrl=self.url)

    def loadCSS(self, path, name='css'):
        path = QFile(path)
        if not path.open(QFile.ReadOnly | QFile.Text):
            return
        css = path.readAll().data().decode("utf-8")

        SCRIPT = """
        (function() {
        css = document.createElement('style');
        css.type = 'text/css';
        css.id = "%s";
        document.head.appendChild(css);
        css.innerText = `%s`;
        })()
        """ % (name, css)

        script = QWebEngineScript()
        self.page().runJavaScript(
                SCRIPT, QWebEngineScript.ApplicationWorld)
        script.setName(name)
        script.setSourceCode(SCRIPT)
        script.setInjectionPoint(QWebEngineScript.DocumentReady)
        script.setRunsOnSubFrames(True)
        script.setWorldId(QWebEngineScript.ApplicationWorld)
        self.page().scripts().insert(script)
