import sys

from PySide2.QtCore import QDir
from PySide2.QtGui import QImageWriter
from PySide2.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QAction, qApp, QMenu, QFileDialog, QMessageBox

from ScribbleArea import ScribbleArea


class Mainwindow(QMainWindow):
    def __init__(self, parent=None):
        super(Mainwindow, self).__init__(parent)
        self.scribbleArea = ScribbleArea()
        self.setCentralWidget(self.scribbleArea)
        self.saveAsActs = []
        self.createActions()
        self.createMenus()

        self.setWindowTitle("Finger Paint")
        self.resize(500, 500)

    #
    #
    # def closeEvent(selfQCloseEvent *event)
    # {
    #     if (maybeSave()) {
    #         event.accept()
    #     } else {
    #         event.ignore()
    #     }
    # }
    #
    def open(self):
        if (self.maybeSave()):
            fileName = QFileDialog.getOpenFileName(self,
                                                   "Open File", QDir.currentPath())
            if not fileName.isEmpty():
                self.scribbleArea.openImage(fileName)


    def save(self):
        action = self.sender()
        fileFormat = action.data().toByteArray()
        self.saveFile(fileFormat)


    def about(self):
        QMessageBox.about(self, "About Scribble",
                "<p>The <b>Scribble</b> example shows how to use QMainWindow as the "
                   "base widget for an application, and how to reimplement some of "
                   "QWidget's event handlers to receive the events generated for "
                   "the application's widgets:</p><p> We reimplement the mouse event "
                   "handlers to facilitate drawing, the paint event handler to "
                   "update the application and the resize event handler to optimize "
                   "the application's appearance. In addition we reimplement the "
                   "close event handler to intercept the close events before "
                   "terminating the application.</p><p> The example also demonstrates "
                   "how to use QPainter to draw an image in real time, as well as "
                   "to repaint widgets.</p>")



    def createActions(self):

        self.openAct = QAction("&Open...", self)
        self.openAct.setShortcut("Ctrl+O")
        self.openAct.triggered.connect(self.open)

        for format in QImageWriter.supportedImageFormats():
            text = "%s... " % str(format).upper()

            action = QAction(text, self)
            action.setData(format)
            action.triggered.connect(self.save)
            self.saveAsActs.append(action)

        self.printAct = QAction("&Print...", self)
        self.printAct.triggered.connect(self.scribbleArea.s_print)

        self.exitAct = QAction("E&xit", self)
        self.exitAct.setShortcut("Ctrl+Q")
        self.exitAct.triggered.connect(self.close)

        self.clearScreenAct = QAction("&Clear Screen", self)
        self.clearScreenAct.setShortcut("Ctrl+L")
        self.clearScreenAct.triggered.connect(self.scribbleArea.clearImage)

        self.aboutAct = QAction("&About", self)
        self.aboutAct.triggered.connect(self.about)

        self.aboutQtAct = QAction("About &Qt", self)
        self.aboutQtAct.triggered.connect(qApp.aboutQt)

    def createMenus(self):
        self.saveAsMenu = QMenu("&Save As", self)
        for action in self.saveAsActs:
            self.saveAsMenu.addAction(action)

        fileMenu = QMenu("&File", self)
        fileMenu.addAction(self.openAct)
        fileMenu.addMenu(self.saveAsMenu)
        fileMenu.addAction(self.printAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        optionMenu = QMenu("&Options", self)
        optionMenu.addAction(self.clearScreenAct)

        helpMenu = QMenu("&Help", self)
        helpMenu.addAction(self.aboutAct)
        helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(fileMenu)
        self.menuBar().addMenu(optionMenu)
        self.menuBar().addMenu(helpMenu)


#
# def maybeSave(self)
# {
#     if (self.scribbleArea.isModified()) {
#        QMessageBox.StandardButton ret
#        ret = QMessageBox.warning(self, tr("Scribble"),
#                           tr("The image has been modified.\n"
#                              "Do you want to save your changes?"),
#                           QMessageBox.Save | QMessageBox.Discard
#                           | QMessageBox.Cancel)
#         if (ret == QMessageBox.Save) {
#             return saveFile("png")
#         } else if (ret == QMessageBox.Cancel) {
#             return false
#         }
#     }
#     return true
# }
#
# def saveFile(self, const QByteArray &fileFormat)
# {
#     QString initialPath = QDir.currentPath() + "/untitled." + fileFormat
#
#     QString fileName = QFileDialog.getSaveFileName(self, tr("Save As"),
#                                initialPath,
#                                tr("%1 Files (*.%2)All Files (*)")
#                                .arg(QString(fileFormat.toUpper()))
#                                .arg(QString(fileFormat)))
#     if (fileName.isEmpty()) {
#         return false
#     } else {
#         return self.scribbleArea.saveImage(fileName, fileFormat)
#     }
# }

if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = Mainwindow()
    m.show()
    app.exec_()
