from PyQt5 import QtCore, QtGui, QtWidgets
import re
from app.utils.db_manager import DBManager
import hashlib

class RegisterPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(RegisterPage, self).__init__()
        self.parent = parent
        self.setupUi()
        
    def setupUi(self):
        # Set the main window properties
        self.setObjectName("RegisterForm")
        self.setWindowTitle("Register - Sales and Inventory Management System")
        self.resize(1280, 720)
        self.setMinimumSize(QtCore.QSize(1280, 720))
        self.setMaximumSize(QtCore.QSize(1280, 720))
        self.setStyleSheet("background-color: #FFFFFF;")
        
        # Create main layout
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Left panel (Brand/Logo section) - similar style to login page
        self.create_brand_panel()
        
        # Right panel (Registration form)
        self.create_register_panel()
        
    def create_brand_panel(self):
        # Left panel for branding - similar to login page
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
        
        self.layout.addWidget(self.left_panel)
        
    def create_register_panel(self):
        # Right panel for registration form
        self.right_panel = QtWidgets.QWidget()
        self.right_panel.setStyleSheet("background-color: white;")
        
        # Registration container - increase height to fit all elements
        self.register_container = QtWidgets.QWidget(self.right_panel)
        self.register_container.setGeometry(QtCore.QRect(80, 60, 480, 600))
        
        # Registration heading
        self.register_label = QtWidgets.QLabel(self.register_container)
        self.register_label.setGeometry(QtCore.QRect(0, 0, 480, 60))
        self.register_label.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
        self.register_label.setText("Create Staff Account")
        self.register_label.setStyleSheet("color: #232323;")
        
        # Subheading
        self.subheading_label = QtWidgets.QLabel(self.register_container)
        self.subheading_label.setGeometry(QtCore.QRect(0, 70, 480, 30))
        self.subheading_label.setFont(QtGui.QFont("Segoe UI", 12))
        self.subheading_label.setText("Please fill in the details to register")
        self.subheading_label.setStyleSheet("color: #777777;")
        
        # Full name
        self.full_name_label = QtWidgets.QLabel(self.register_container)
        self.full_name_label.setGeometry(QtCore.QRect(0, 120, 480, 30))
        self.full_name_label.setFont(QtGui.QFont("Segoe UI", 10))
        self.full_name_label.setText("Full Name")
        self.full_name_label.setStyleSheet("color: #555555;")
        
        self.full_name_field = QtWidgets.QLineEdit(self.register_container)
        self.full_name_field.setGeometry(QtCore.QRect(0, 150, 480, 50))
        self.full_name_field.setFont(QtGui.QFont("Segoe UI", 12))
        self.full_name_field.setStyleSheet(
            "border: 1px solid #CCCCCC; "
            "border-radius: 5px; "
            "padding: 10px;"
        )
        self.full_name_field.setPlaceholderText("Enter your full name")
        
        # Username
        self.username_label = QtWidgets.QLabel(self.register_container)
        self.username_label.setGeometry(QtCore.QRect(0, 210, 480, 30))
        self.username_label.setFont(QtGui.QFont("Segoe UI", 10))
        self.username_label.setText("Username")
        self.username_label.setStyleSheet("color: #555555;")
        
        self.username_field = QtWidgets.QLineEdit(self.register_container)
        self.username_field.setGeometry(QtCore.QRect(0, 240, 480, 50))
        self.username_field.setFont(QtGui.QFont("Segoe UI", 12))
        self.username_field.setStyleSheet(
            "border: 1px solid #CCCCCC; "
            "border-radius: 5px; "
            "padding: 10px;"
        )
        self.username_field.setPlaceholderText("Create a username")
        
        # Password
        self.password_label = QtWidgets.QLabel(self.register_container)
        self.password_label.setGeometry(QtCore.QRect(0, 300, 480, 30))
        self.password_label.setFont(QtGui.QFont("Segoe UI", 10))
        self.password_label.setText("Password")
        self.password_label.setStyleSheet("color: #555555;")
        
        self.password_field = QtWidgets.QLineEdit(self.register_container)
        self.password_field.setGeometry(QtCore.QRect(0, 330, 480, 50))
        self.password_field.setFont(QtGui.QFont("Segoe UI", 12))
        self.password_field.setStyleSheet(
            "border: 1px solid #CCCCCC; "
            "border-radius: 5px;"
            "padding: 10px;"
        )
        self.password_field.setPlaceholderText("Create a password")
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        
        # Confirm Password
        self.confirm_password_label = QtWidgets.QLabel(self.register_container)
        self.confirm_password_label.setGeometry(QtCore.QRect(0, 390, 480, 30))
        self.confirm_password_label.setFont(QtGui.QFont("Segoe UI", 10))
        self.confirm_password_label.setText("Confirm Password")
        self.confirm_password_label.setStyleSheet("color: #555555;")
        
        self.confirm_password_field = QtWidgets.QLineEdit(self.register_container)
        self.confirm_password_field.setGeometry(QtCore.QRect(0, 420, 480, 50))
        self.confirm_password_field.setFont(QtGui.QFont("Segoe UI", 12))
        self.confirm_password_field.setStyleSheet(
            "border: 1px solid #CCCCCC; "
            "border-radius: 5px;"
            "padding: 10px;"
        )
        self.confirm_password_field.setPlaceholderText("Confirm your password")
        self.confirm_password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        
        # Error message label (hidden initially) - MOVED below confirm password field
        self.error_label = QtWidgets.QLabel(self.register_container)
        self.error_label.setGeometry(QtCore.QRect(0, 475, 480, 30))  # Keep Y position at 475
        self.error_label.setFont(QtGui.QFont("Segoe UI", 10))
        self.error_label.setText("Error message")
        self.error_label.setStyleSheet("color: #FF3333;")
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)  # Change to center alignment
        self.error_label.hide()
        
        # Register button - moved down to make room for error label
        self.register_button = QtWidgets.QPushButton(self.register_container)
        self.register_button.setGeometry(QtCore.QRect(0, 510, 480, 50))  # Changed Y position to 510
        self.register_button.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Bold))
        self.register_button.setText("Register")
        self.register_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.register_button.setStyleSheet(
            "background-color: #232323; "
            "color: white; "
            "border-radius: 5px; "
            "border: none;"
        )
        self.register_button.clicked.connect(self.register_user)
        
        # Login link - adjusted position
        self.login_link = QtWidgets.QLabel(self.register_container)
        self.login_link.setGeometry(QtCore.QRect(0, 570, 480, 30))  # Changed Y position to 570
        self.login_link.setFont(QtGui.QFont("Segoe UI", 10))
        self.login_link.setText("<a href='#' style='color: #232323; text-decoration: none;'>Already have an account? <span style='color: #232323; font-weight: bold;'>Sign In</span></a>")
        self.login_link.setAlignment(QtCore.Qt.AlignCenter)
        self.login_link.setOpenExternalLinks(False)
        self.login_link.linkActivated.connect(self.back_to_login)
        
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
        
        self.layout.addWidget(self.right_panel)
        
    def register_user(self):
        """Handle user registration"""
        # Get input values
        full_name = self.full_name_field.text().strip()
        username = self.username_field.text().strip()
        password = self.password_field.text()
        confirm_password = self.confirm_password_field.text()
        
        # Basic validation
        if not all([full_name, username, password, confirm_password]):
            self.show_error("Please fill in all fields")
            return
        
        if len(username) < 4:
            self.show_error("Username must be at least 4 characters")
            return
            
        if len(password) < 6:
            self.show_error("Password must be at least 6 characters")
            return
            
        if password != confirm_password:
            self.show_error("Passwords do not match")
            return
        
        # Advanced username validation (alphanumeric and underscores only)
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            self.show_error("Username can only contain letters, numbers, and underscores")
            return
            
        try:
            # Check if username already exists
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                self.show_error("Username is already taken")
                cursor.close()
                return
            
            # Create admin verification dialog
            admin_dialog = QtWidgets.QDialog(self)
            admin_dialog.setWindowTitle("Admin Verification")
            admin_dialog.setFixedSize(400, 300)
            
            # Dialog layout
            layout = QtWidgets.QVBoxLayout(admin_dialog)
            
            # Title label
            title_label = QtWidgets.QLabel("Admin Verification Required")
            title_label.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Bold))
            title_label.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(title_label)
            
            # Description
            desc_label = QtWidgets.QLabel("Please enter admin credentials to continue with staff registration:")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
            
            # Form layout for fields
            form_layout = QtWidgets.QFormLayout()
            
            # Admin username
            admin_username_field = QtWidgets.QLineEdit()
            admin_username_field.setPlaceholderText("Admin username")
            form_layout.addRow("Admin Username:", admin_username_field)
            
            # Admin password
            admin_password_field = QtWidgets.QLineEdit()
            admin_password_field.setEchoMode(QtWidgets.QLineEdit.Password)
            admin_password_field.setPlaceholderText("Admin password")
            form_layout.addRow("Admin Password:", admin_password_field)
            
            # Reason for creation
            reason_field = QtWidgets.QTextEdit()
            reason_field.setPlaceholderText("Enter the reason for creating this account")
            reason_field.setMaximumHeight(80)
            form_layout.addRow("Reason:", reason_field)
            
            layout.addLayout(form_layout)
            
            # Buttons
            button_box = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
            )
            button_box.accepted.connect(admin_dialog.accept)
            button_box.rejected.connect(admin_dialog.reject)
            layout.addWidget(button_box)
            
            # Show the dialog
            if admin_dialog.exec_() != QtWidgets.QDialog.Accepted:
                return
            
            # Verify admin credentials
            admin_username = admin_username_field.text().strip()
            admin_password = admin_password_field.text()
            reason = reason_field.toPlainText().strip()
            
            if not admin_username or not admin_password:
                self.show_error("Admin credentials are required")
                return
                
            if not reason:
                self.show_error("Reason for account creation is required")
                return
            
            # Verify admin credentials in the database
            from app.utils.auth_manager import AuthManager
            auth_manager = AuthManager()
            admin = auth_manager._auth_strategy.authenticate(admin_username, admin_password)
            
            if not admin or admin.role != 'admin':
                self.show_error("Invalid admin credentials")
                return
            
            # Hash the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            # Get the admin's user_id
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (admin_username,))
            admin_data = cursor.fetchone()
            admin_id = admin_data['user_id']

            # Insert new user with staff role, reason, and created_by
            cursor.execute(
                "INSERT INTO users (username, password, full_name, role, reason_for_creation, created_by) VALUES (%s, %s, %s, %s, %s, %s)",
                (username, hashed_password, full_name, 'staff', reason, admin_id)
            )
            
            conn.commit()
            cursor.close()
            
            # Show success message
            QtWidgets.QMessageBox.information(
                self, 
                "Registration Successful", 
                f"Staff account for {full_name} has been created successfully."
            )
            
            # Return to login page
            self.back_to_login()
            
        except Exception as e:
            self.show_error(f"Registration failed: {str(e)}")
            print(f"Registration error: {e}")
    
    def show_error(self, message):
        """Display error message"""
        self.error_label.setText(message)
        self.error_label.show()
        
        # Hide after 3 seconds
        QtCore.QTimer.singleShot(3000, self.error_label.hide)
        
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
                admin_info = "For register assistance, please contact:\n"
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
    
    def back_to_login(self):
        """Return to the login page"""
        if self.parent:
            self.parent.show()
            print("Returning to login page") # Add this for debugging
        else:
            # If parent reference is lost, create a new login page
            from app.ui.pages.login_page import LoginPage
            login_window = LoginPage()
            login_window.show()
            print("Creating new login page") # Add this for debugging
        self.close()