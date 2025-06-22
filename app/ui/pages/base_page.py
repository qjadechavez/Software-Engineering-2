from PyQt5 import QtWidgets, QtCore, QtGui

class BasePage(QtWidgets.QWidget):
    """Base class for all pages in the application."""
    
    def __init__(self, parent=None, title="Page", user_info=None):
        super(BasePage, self).__init__(parent)
        self.title = title
        self.user_info = user_info
        self.setupUi()
        
    def setupUi(self):
        """Set up the UI for this page. Override in subclasses."""
        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
          # Create content area - to be overridden by subclasses
        self.createContent()
        
    def createContent(self):
        # This method should be overridden by subclasses
        pass
    
    def set_user_info(self, user_info):
        self.user_info = user_info