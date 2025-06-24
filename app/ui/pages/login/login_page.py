from PyQt5 import QtCore, QtGui, QtWidgets
from app.ui.main_window import MainWindow
from .style_factory import StyleFactory
from .form_factory import FormFactory
from .handlers.auth_handler import AuthHandler

class LoginPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LoginPage, self).__init__(parent)
        self.setupUi()
        # Create auth handler
        self.auth_handler = AuthHandler(self)
        
    def setupUi(self):
        # Set the main window properties
        self.setObjectName("LoginForm")
        self.setWindowTitle("Login - Sales and Inventory Management System")
        self.resize(1280, 720)
        self.setMinimumSize(QtCore.QSize(1280, 720))
        self.setMaximumSize(QtCore.QSize(1280, 720))
        self.setStyleSheet("background-color: #FFFFFF;")
        
        # Create main layout
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Create panels
        self.create_brand_panel()
        self.create_login_panel()
        
    def create_brand_panel(self):
        # Left panel for branding
        self.left_panel = QtWidgets.QWidget()
        self.left_panel.setFixedWidth(640)
        self.left_panel.setStyleSheet("background-color: #232323;")
        
        # Logo/Brand image
        self.logo_label = QtWidgets.QLabel(self.left_panel)
        self.logo_label.setGeometry(QtCore.QRect(140, 100, 400, 400))
        pixmap = QtGui.QPixmap("app/resources/images/logo/login-logo.png")
        scaled_pixmap = pixmap.scaled(350, 350, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.logo_label.setPixmap(scaled_pixmap)        

        # Brand tagline
        self.tagline_label = QtWidgets.QLabel(self.left_panel)
        self.tagline_label.setGeometry(QtCore.QRect(120, 420, 400, 40))
        self.tagline_label.setStyleSheet("color: #E2F163; font-size: 18px;")
        self.tagline_label.setFont(QtGui.QFont("Segoe UI", 14))
        self.tagline_label.setText("Sales and Inventory Management System")
        self.tagline_label.setAlignment(QtCore.Qt.AlignCenter)

        # Help button with icon
        self.help_button = FormFactory.create_button(
            self.left_panel, 
            "  Need Help?", 
            primary=False, 
            icon_path="app/resources/images/help_icon.png"
        )
        self.help_button.setGeometry(QtCore.QRect(30, 650, 160, 45))
        self.help_button.clicked.connect(self.show_help)
        
        self.layout.addWidget(self.left_panel)
        
    def create_login_panel(self):
        # Right panel for login form
        self.right_panel = QtWidgets.QWidget()
        self.right_panel.setStyleSheet("background-color: white;")
        
        # Login container
        self.login_container = QtWidgets.QWidget(self.right_panel)
        self.login_container.setGeometry(QtCore.QRect(120, 150, 400, 420))
        
        # Welcome heading
        self.welcome_label = FormFactory.create_label(
            self.login_container, 
            "Welcome Back!", 
            font_size=24, 
            bold=True
        )
        self.welcome_label.setGeometry(QtCore.QRect(0, 0, 400, 60))
        self.welcome_label.setStyleSheet("color: #232323;")
        
        # Subheading
        self.subheading_label = FormFactory.create_label(
            self.login_container, 
            "Please sign in to continue", 
            font_size=12
        )
        self.subheading_label.setGeometry(QtCore.QRect(0, 70, 400, 30))
        self.subheading_label.setStyleSheet("color: #777777;")
        
        # Username label
        self.username_label = FormFactory.create_label(self.login_container, "Username")
        self.username_label.setGeometry(QtCore.QRect(0, 130, 400, 30))
        
        # Username field
        self.username_field = FormFactory.create_input_field(
            self.login_container,
            placeholder="Enter your username"
        )
        self.username_field.setGeometry(QtCore.QRect(0, 160, 400, 50))
        
        # Password label
        self.password_label = FormFactory.create_label(self.login_container, "Password")
        self.password_label.setGeometry(QtCore.QRect(0, 220, 400, 30))
        
        # Password field
        self.password_field = FormFactory.create_input_field(
            self.login_container,
            placeholder="Enter your password",
            password_mode=True
        )
        self.password_field.setGeometry(QtCore.QRect(0, 250, 400, 50))
        
        # Error message label (hidden initially)
        self.error_label = QtWidgets.QLabel(self.login_container)
        self.error_label.setGeometry(QtCore.QRect(0, 305, 400, 30))
        self.error_label.setFont(QtGui.QFont("Segoe UI", 10))
        self.error_label.setText("Invalid username or password")
        self.error_label.setStyleSheet(StyleFactory.get_error_style())
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        self.error_label.hide()
        
        # Login button
        self.login_button = FormFactory.create_button(self.login_container, "Login")
        self.login_button.setGeometry(QtCore.QRect(0, 340, 400, 50))
        self.login_button.clicked.connect(self.authenticate)
        
        # Register account link
        register_link_text = (
            "<a href='#' style='color: #232323; text-decoration: none;'>"
            "Don't have an account? <span style='color: #232323; font-weight: bold;'>"
            "Register Here</span></a>"
        )
        self.register_link = FormFactory.create_link_label(self.login_container, register_link_text)
        self.register_link.setGeometry(QtCore.QRect(0, 395, 400, 30))
        self.register_link.linkActivated.connect(self.show_registration_page)
        
        # Add right panel to main layout
        self.layout.addWidget(self.right_panel)
        
    def authenticate(self):
        """Handle authentication when login button is pressed"""
        username = self.username_field.text()
        password = self.password_field.text()
        
        user = self.auth_handler.authenticate(username, password)
        
        if user:
            self.open_main_window(user)
        
    def show_error(self, message):
        """Display error message"""
        self.error_label.setText(message)
        self.error_label.show()
        
        QtCore.QTimer.singleShot(3000, self.error_label.hide)
        
    def open_main_window(self, user):
        """Open the main application window after successful login"""
        # Create and show the main window 
        self.main_window = MainWindow(user_info=user)
        self.main_window.show()
        self.hide() 

    def show_help(self):
        """Show help dialog when help button is clicked"""
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Help Information")
        
        # Get admin contacts from the handler
        admins = self.auth_handler.get_admin_contacts()
        
        if admins:
            admin_info = "For login assistance, please contact:\n"
            for admin in admins:
                admin_info += f"• {admin['full_name']} ({admin['role'].capitalize()})\n"
            admin_info += "\nOr reach out to the IT support team."
            msg.setInformativeText(admin_info)
        else:
            # Fallback if no admins found
            msg.setInformativeText("For login assistance, please contact your system administrator or IT support team.")
        
        msg.setWindowTitle("Help")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def show_registration_page(self):
        """Open registration form"""
        # Import here to avoid circular imports
        from app.ui.pages.register.register_page import RegisterPage
        self.register_window = RegisterPage(parent=self)
        self.register_window.show()
        self.hide()