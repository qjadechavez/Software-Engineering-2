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
        
        # Create header
        self.createHeader()
        
        # Create content area - to be overridden by subclasses
        self.createContent()
    
    def createHeader(self):
        # Header widget with gradient background
        self.widget_header = QtWidgets.QWidget()
        self.widget_header.setObjectName("widget_header")
        self.widget_header.setFixedHeight(99)
        self.widget_header.setStyleSheet("""
            QWidget#widget_header {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #232323, stop:1 #3f3f3f);
                border-bottom: 2px solid #3a3a3a;
            }
        """)
        
        # Set fixed layout for header
        header_layout = QtWidgets.QHBoxLayout(self.widget_header)
        header_layout.setContentsMargins(25, 0, 25, 0)
        header_layout.setSpacing(10)
        
        # Add title to header (left side - fixed position)
        self.header_title = QtWidgets.QLabel(self.title)
        self.header_title.setObjectName("header_title")
        self.header_title.setStyleSheet("""
            color: white; 
            font-size: 26px;
            padding-left: 10px;
            border-left: 4px solid #4ecca3;
        """)
        self.header_title.setFont(QtGui.QFont("Segoe UI", 20, QtGui.QFont.Bold))
        self.header_title.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.header_title.setFixedWidth(320)
        
        # Add user info to header (center - fixed position)
        self.user_info_container = QtWidgets.QWidget()
        self.user_info_container.setFixedWidth(320)
        self.user_info_container.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        user_info_layout = QtWidgets.QVBoxLayout(self.user_info_container)
        user_info_layout.setContentsMargins(0, 15, 0, 15)
        user_info_layout.setSpacing(3)
        
        # User label (upper part)
        self.user_label = QtWidgets.QLabel("CURRENT USER")
        self.user_label.setStyleSheet("color: #a0a0a0; font-size: 11px; letter-spacing: 1px;")
        self.user_label.setAlignment(QtCore.Qt.AlignCenter)
        self.user_label.setFont(QtGui.QFont("Segoe UI", 9))
        
        # User info label (lower part)
        self.user_info_label = QtWidgets.QLabel()
        self.user_info_label.setObjectName("user_info_label")
        self.user_info_label.setStyleSheet("color: #ffffff; font-size: 14px;")
        self.user_info_label.setFont(QtGui.QFont("Segoe UI", 13, QtGui.QFont.DemiBold))
        self.user_info_label.setAlignment(QtCore.Qt.AlignCenter)
        
        # Add labels to container
        user_info_layout.addWidget(self.user_label)
        user_info_layout.addWidget(self.user_info_label)
        
        # Add date/time to header (right side - fixed position)
        self.header_date_container = QtWidgets.QWidget()
        self.header_date_container.setFixedWidth(320)
        
        date_layout = QtWidgets.QVBoxLayout(self.header_date_container)
        date_layout.setContentsMargins(0, 15, 0, 15)
        date_layout.setSpacing(3)
        
        # Date label (upper part)
        self.date_label = QtWidgets.QLabel("CURRENT DATE")
        self.date_label.setStyleSheet("color: #a0a0a0; font-size: 11px; letter-spacing: 1px;")
        self.date_label.setAlignment(QtCore.Qt.AlignRight)
        self.date_label.setFont(QtGui.QFont("Segoe UI", 9))
        
        # Date value (lower part)
        self.header_date = QtWidgets.QLabel()
        self.header_date.setObjectName("header_date")
        self.header_date.setStyleSheet("color: #4ecca3; font-size: 14px;")
        self.header_date.setFont(QtGui.QFont("Segoe UI", 13))
        self.header_date.setAlignment(QtCore.Qt.AlignRight)
        
        # Add labels to container
        date_layout.addWidget(self.date_label)
        date_layout.addWidget(self.header_date)
        
        # Add widgets to layout with proper alignment
        header_layout.addWidget(self.header_title, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        header_layout.addStretch(1)  # Flexible space
        header_layout.addWidget(self.user_info_container, 0, QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        header_layout.addStretch(1)  # Flexible space
        header_layout.addWidget(self.header_date_container, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        # Update content of user info and date
        self.update_user_info()
        self.update_datetime()
        
        # Create timer to update date/time
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(60000)  # Update every minute
        
        self.layout.addWidget(self.widget_header)

    def createContent(self):
        # This method should be overridden by subclasses
        pass
    
    def update_datetime(self):
        current_datetime = QtCore.QDateTime.currentDateTime()
        formatted_datetime = current_datetime.toString("dddd, MMMM d, yyyy")
        self.header_date.setText(formatted_datetime)
    
    def update_user_info(self):
        if self.user_info:
            role = self.user_info.get("role", "").capitalize()
            username = self.user_info.get("username", "")
            self.user_info_label.setText(f"{username} | {role}")
        else:
            self.user_info_label.setText("Not logged in")
    
    def set_user_info(self, user_info):
        self.user_info = user_info
        self.update_user_info()