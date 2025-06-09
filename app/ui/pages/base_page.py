from PyQt5 import QtWidgets, QtCore, QtGui

class BasePage(QtWidgets.QWidget):
    """Base class for all pages in the application."""
    
    def __init__(self, parent=None):
        super(BasePage, self).__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        """Set up the UI for this page. Override in subclasses."""
        pass