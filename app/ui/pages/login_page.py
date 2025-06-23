from PyQt5 import QtCore, QtGui, QtWidgets
from app.ui.main_window import MainWindow
from app.utils.auth_manager import AuthManager
from app.ui.pages.register.register_page import RegisterPage

class LoginPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LoginPage, self).__init__(parent)
        # Create the main window
        self.setupUi()
        # Create auth manager
        self.auth_manager = AuthManager()
        
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
        
        # Login container
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
            "border-radius: 5px;"
            "padding: 10px;"
        )
        self.password_field.setPlaceholderText("Enter your password")
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        
        # Error message label (hidden initially) - MOVED below password field
        self.error_label = QtWidgets.QLabel(self.login_container)
        self.error_label.setGeometry(QtCore.QRect(0, 305, 400, 30))  # Changed Y position to 305
        self.error_label.setFont(QtGui.QFont("Segoe UI", 10))
        self.error_label.setText("Invalid username or password")
        self.error_label.setStyleSheet("color: #FF3333;")
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        self.error_label.hide()
        
        # Login button - moved down to make room for error label
        self.login_button = QtWidgets.QPushButton(self.login_container)
        self.login_button.setGeometry(QtCore.QRect(0, 340, 400, 50))  # Changed Y position to 340
        self.login_button.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Bold))
        self.login_button.setText("Login")
        self.login_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.login_button.setStyleSheet(
            "background-color: #232323; "
            "color: white; "
            "border-radius: 5px; "
            "border: none;"
        )
        
        # Register account link - adjusted position
        self.register_link = QtWidgets.QLabel(self.login_container)
        self.register_link.setGeometry(QtCore.QRect(0, 390, 400, 30))  # No change needed, but kept at position 390
        self.register_link.setFont(QtGui.QFont("Segoe UI", 10))
        self.register_link.setText("<a href='#' style='color: #232323; text-decoration: none;'>Don't have an account? <span style='color: #232323; font-weight: bold;'>Register Here</span></a>")
        self.register_link.setAlignment(QtCore.Qt.AlignCenter)
        self.register_link.setOpenExternalLinks(False)
        self.register_link.linkActivated.connect(self.show_registration_page)
        
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
            
        try:
            # Lazy initialization of auth manager
            if self.auth_manager is None:
                self.auth_manager = AuthManager()
            # Authenticate user
            user = self.auth_manager.authenticate(username, password)
            
            if user:
                self.open_main_window(user)
            else:
                self.show_error("Invalid username or password")
        except Exception as e:
            self.show_error(f"Login error: Database connection failed")
            print(f"Authentication error: {e}")
        
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
        
        # Attempt to retrieve admin user information from the database        
        try:
            from app.utils.db_manager import DBManager
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Query for admin users
            cursor.execute("SELECT username, full_name, role FROM users WHERE role = 'admin'")
            admins = cursor.fetchall()
            cursor.close()
            
            if admins:
                admin_info = "For login assistance, please contact:\n"
                for admin in admins:
                    admin_info += f"• {admin['full_name']} ({admin['role'].capitalize()})\n"
                admin_info += "\nOr reach out to the IT support team."
                msg.setInformativeText(admin_info)
            else:
                # Fallback if no admins found
                msg.setInformativeText("For login assistance, please contact your system administrator or IT support team.")
        
        except Exception as e:
            print(f"Error retrieving admin information: {e}")
            # Fallback in case of database error
            msg.setInformativeText("For login assistance, please contact Juan (Admin) or IT support team.")
        
        msg.setWindowTitle("Help")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def show_registration_page(self):
        """Open registration form"""
        self.register_window = RegisterPage(parent=self)
        self.register_window.show()
        self.hide()