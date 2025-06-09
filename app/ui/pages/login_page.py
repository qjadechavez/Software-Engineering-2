from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from app.ui.main_window import Ui_MainWindow
from app.utils.auth_manager import AuthManager

class LoginPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LoginPage, self).__init__(parent)
        self.setupUi()
        
        # Create auth manager
        self.auth_manager = AuthManager()
        
    def setupUi(self):
        # Set the main window properties
        self.setObjectName("LoginForm")
        self.resize(1280, 720)
        self.setMinimumSize(QtCore.QSize(1280, 720))
        self.setMaximumSize(QtCore.QSize(1280, 720))
        self.setStyleSheet("background-color: #FFFFFF;")
        
        # Create main layout
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Left panel (Brand/Logo section)
        self.create_brand_panel()
        
        # Right panel (Login form)
        self.create_login_panel()
        
    def create_brand_panel(self):
        # Left panel for branding
        self.left_panel = QtWidgets.QWidget()
        self.left_panel.setFixedWidth(640)
        self.left_panel.setStyleSheet("background-color: #232323;")
        
        # Logo/Brand image
        self.logo_label = QtWidgets.QLabel(self.left_panel)
        self.logo_label.setGeometry(QtCore.QRect(195, 200, 250, 250))
        pixmap = QtGui.QPixmap("app/resources/images/Miere1.png")
        scaled_pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.logo_label.setPixmap(scaled_pixmap)        

        # Brand tagline
        self.tagline_label = QtWidgets.QLabel(self.left_panel)
        self.tagline_label.setGeometry(QtCore.QRect(120, 400, 400, 40))
        self.tagline_label.setStyleSheet("color: #E2F163; font-size: 18px;")
        self.tagline_label.setFont(QtGui.QFont("Segoe UI", 14))
        self.tagline_label.setText("Inventory Management System")
        self.tagline_label.setAlignment(QtCore.Qt.AlignCenter)

        # Improved help button with icon
        self.help_button = QtWidgets.QPushButton(self.left_panel)
        self.help_button.setGeometry(QtCore.QRect(30, 650, 150, 45))
        self.help_button.setFont(QtGui.QFont("Segoe UI", 10))
        self.help_button.setText("  Need Help?")
        self.help_button.setIcon(QtGui.QIcon("app/resources/images/help_icon.png"))
        self.help_button.setIconSize(QtCore.QSize(20, 20))
        self.help_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.help_button.setStyleSheet(
            "QPushButton {"
            "    background-color: rgba(226, 241, 99, 0.15); "
            "    color: #E2F163; "
            "    border: 1px solid #E2F163; "
            "    border-radius: 22px; "
            "    padding: 8px 15px;"
            "    text-align: left;"
            "}"
            "QPushButton:hover {"
            "    background-color: rgba(226, 241, 99, 0.25); "
            "}"
            "QPushButton:pressed {"
            "    background-color: rgba(226, 241, 99, 0.35); "
            "}"
        )
        self.help_button.clicked.connect(self.show_help)
        
        self.layout.addWidget(self.left_panel)
        
    def create_login_panel(self):
        # Right panel for login form
        self.right_panel = QtWidgets.QWidget()
        self.right_panel.setStyleSheet("background-color: white;")
        
        # Login container - centers the login form
        self.login_container = QtWidgets.QWidget(self.right_panel)
        self.login_container.setGeometry(QtCore.QRect(120, 150, 400, 420))
        
        # Welcome heading
        self.welcome_label = QtWidgets.QLabel(self.login_container)
        self.welcome_label.setGeometry(QtCore.QRect(0, 0, 400, 60))
        self.welcome_label.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
        self.welcome_label.setText("Welcome Back!")
        self.welcome_label.setStyleSheet("color: #232323;")
        
        # Subheading
        self.subheading_label = QtWidgets.QLabel(self.login_container)
        self.subheading_label.setGeometry(QtCore.QRect(0, 70, 400, 30))
        self.subheading_label.setFont(QtGui.QFont("Segoe UI", 12))
        self.subheading_label.setText("Please sign in to continue")
        self.subheading_label.setStyleSheet("color: #777777;")
        
        # Username label
        self.username_label = QtWidgets.QLabel(self.login_container)
        self.username_label.setGeometry(QtCore.QRect(0, 130, 400, 30))
        self.username_label.setFont(QtGui.QFont("Segoe UI", 10))
        self.username_label.setText("Username")
        self.username_label.setStyleSheet("color: #555555;")
        
        # Username field
        self.username_field = QtWidgets.QLineEdit(self.login_container)
        self.username_field.setGeometry(QtCore.QRect(0, 160, 400, 50))
        self.username_field.setFont(QtGui.QFont("Segoe UI", 12))
        self.username_field.setStyleSheet(
            "border: 1px solid #CCCCCC; "
            "border-radius: 5px; "
            "padding: 10px;"
        )
        self.username_field.setPlaceholderText("Enter your username")
        
        # Password label
        self.password_label = QtWidgets.QLabel(self.login_container)
        self.password_label.setGeometry(QtCore.QRect(0, 220, 400, 30))
        self.password_label.setFont(QtGui.QFont("Segoe UI", 10))
        self.password_label.setText("Password")
        self.password_label.setStyleSheet("color: #555555;")
        
        # Password field
        self.password_field = QtWidgets.QLineEdit(self.login_container)
        self.password_field.setGeometry(QtCore.QRect(0, 250, 400, 50))
        self.password_field.setFont(QtGui.QFont("Segoe UI", 12))
        self.password_field.setStyleSheet(
            "border: 1px solid #CCCCCC; "
            "border-radius: 5px; "
            "padding: 10px;"
        )
        self.password_field.setPlaceholderText("Enter your password")
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        
        # Login button
        self.login_button = QtWidgets.QPushButton(self.login_container)
        self.login_button.setGeometry(QtCore.QRect(0, 330, 400, 50))
        self.login_button.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Bold))
        self.login_button.setText("Login")
        self.login_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.login_button.setStyleSheet(
            "background-color: #232323; "
            "color: white; "
            "border-radius: 5px; "
            "border: none;"
        )
        
        # Error message label (hidden initially)
        self.error_label = QtWidgets.QLabel(self.login_container)
        self.error_label.setGeometry(QtCore.QRect(0, 390, 400, 30))
        self.error_label.setFont(QtGui.QFont("Segoe UI", 10))
        self.error_label.setText("Invalid username or password")
        self.error_label.setStyleSheet("color: #FF3333;")
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        self.error_label.hide()
        
        # Connect login button to authentication function
        self.login_button.clicked.connect(self.authenticate)
        
        # Add right panel to main layout
        self.layout.addWidget(self.right_panel)
        
    def authenticate(self):
        """Handle authentication when login button is pressed"""
        username = self.username_field.text()
        password = self.password_field.text()
        
        # Validate input
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
            
        # Authenticate user
        user = self.auth_manager.authenticate(username, password)
        
        if user:
            self.open_main_window()
        else:
            self.show_error("Invalid username or password")
            
    def show_error(self, message):
        """Display error message"""
        self.error_label.setText(message)
        self.error_label.show()
        
        # Hide the error message after 3 seconds
        QtCore.QTimer.singleShot(3000, self.error_label.hide)
        
    def open_main_window(self):
        """Open the main application window after successful login"""
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
        self.main_window.show()
        self.hide() 

    def show_help(self):
        """Show help dialog when help button is clicked"""
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Help Information")
        msg.setInformativeText("For login assistance, please contact your system administrator or IT support team.")
        msg.setWindowTitle("Help")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()