from PyQt5 import QtWidgets, QtCore, QtGui

class BasePage(QtWidgets.QWidget):
    """Base class for all pages in the application."""
    
    def __init__(self, parent=None, title="Page"):
        super(BasePage, self).__init__(parent)
        self.title = title
        self.setupUi()
        
    def setupUi(self):
        """Set up the UI for this page. Override in subclasses."""
        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Create header
        self.createHeader()
        
        # Create content area - to be overridden by subclasses
        self.createContent()
    
    def createHeader(self):
        # Header widget
        self.widget_header = QtWidgets.QWidget()
        self.widget_header.setObjectName("widget_header")
        self.widget_header.setFixedHeight(99)
        self.widget_header.setStyleSheet("background-color: rgba(35, 35, 35, 0.95);")
        
        # Add title to header
        self.header_layout = QtWidgets.QHBoxLayout(self.widget_header)
        self.header_layout.setContentsMargins(20, 0, 20, 0)
        
        self.header_title = QtWidgets.QLabel(self.title)
        self.header_title.setObjectName("header_title")
        self.header_title.setStyleSheet("color: white; font-size: 24px;")
        self.header_title.setFont(QtGui.QFont("Segoe UI", 18, QtGui.QFont.Bold))
        self.header_title.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.header_layout.addWidget(self.header_title)
        self.header_layout.addStretch()
        
        # Add date/time to header
        self.header_date = QtWidgets.QLabel()
        self.header_date.setObjectName("header_date")
        self.header_date.setStyleSheet("color: #E2F163; font-size: 14px;")
        self.header_date.setFont(QtGui.QFont("Segoe UI", 12))
        self.header_date.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.update_datetime()
        
        # Create timer to update date/time
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(60000)  # Update every minute
        
        self.header_layout.addWidget(self.header_date)
        
        self.layout.addWidget(self.widget_header)
    
    def createContent(self):
        # This method should be overridden by subclasses
        pass
    
    def update_datetime(self):
        current_datetime = QtCore.QDateTime.currentDateTime()
        formatted_datetime = current_datetime.toString("dddd, MMMM d, yyyy")
        self.header_date.setText(formatted_datetime)