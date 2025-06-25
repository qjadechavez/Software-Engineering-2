from PyQt5 import QtCore, QtGui, QtWidgets
import re
import hashlib
from app.utils.db_manager import DBManager
from .style_factory import StyleFactory
from .form_factory import FormFactory
from .dialogs.admin_verification_dialog import AdminVerificationDialog

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
        
        # Left panel (Brand/Logo section)
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
        
    def create_register_panel(self):
        # Right panel for registration form
        self.right_panel = QtWidgets.QWidget()
        self.right_panel.setStyleSheet("background-color: white;")
        
        # Registration container
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
        self.full_name_label = FormFactory.create_label(self.register_container, "Full Name")
        self.full_name_label.setGeometry(QtCore.QRect(0, 120, 480, 30))
        
        self.full_name_field = FormFactory.create_input_field(
            self.register_container,
            placeholder="Enter your full name"
        )
        self.full_name_field.setGeometry(QtCore.QRect(0, 150, 480, 50))
        
        # Username
        self.username_label = FormFactory.create_label(self.register_container, "Username")
        self.username_label.setGeometry(QtCore.QRect(0, 210, 480, 30))
        
        self.username_field = FormFactory.create_input_field(
            self.register_container,
            placeholder="Create a username"
        )
        self.username_field.setGeometry(QtCore.QRect(0, 240, 480, 50))
        
        # Password
        self.password_label = FormFactory.create_label(self.register_container, "Password")
        self.password_label.setGeometry(QtCore.QRect(0, 300, 480, 30))
        
        self.password_field = FormFactory.create_input_field(
            self.register_container,
            placeholder="Create a password",
            password_mode=True
        )
        self.password_field.setGeometry(QtCore.QRect(0, 330, 480, 50))
        
        # Confirm Password
        self.confirm_password_label = FormFactory.create_label(self.register_container, "Confirm Password")
        self.confirm_password_label.setGeometry(QtCore.QRect(0, 390, 480, 30))
        
        self.confirm_password_field = FormFactory.create_input_field(
            self.register_container,
            placeholder="Confirm your password",
            password_mode=True
        )
        self.confirm_password_field.setGeometry(QtCore.QRect(0, 420, 480, 50))
        
        # Error message label (hidden initially)
        self.error_label = QtWidgets.QLabel(self.register_container)
        self.error_label.setGeometry(QtCore.QRect(0, 475, 480, 30))
        self.error_label.setFont(QtGui.QFont("Segoe UI", 10))
        self.error_label.setText("Error message")
        self.error_label.setStyleSheet(StyleFactory.get_error_style())
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        self.error_label.hide()
        
        # Register button
        self.register_button = FormFactory.create_button(self.register_container, "Register")
        self.register_button.setGeometry(QtCore.QRect(0, 510, 480, 50))
        self.register_button.clicked.connect(self.register_user)
        
        # Login link
        self.login_link = QtWidgets.QLabel(self.register_container)
        self.login_link.setGeometry(QtCore.QRect(0, 570, 480, 30))
        self.login_link.setFont(QtGui.QFont("Segoe UI", 10))
        self.login_link.setText("<a href='#' style='color: #232323; text-decoration: none;'>Already have an account? <span style='color: #232323; font-weight: bold;'>Sign In</span></a>")
        self.login_link.setAlignment(QtCore.Qt.AlignCenter)
        self.login_link.setOpenExternalLinks(False)
        self.login_link.linkActivated.connect(self.back_to_login)
        
        self.layout.addWidget(self.right_panel)
        
    def register_user(self):
        """Handle user registration with improved structure and error handling"""
        # Get and validate input values
        validation_result = self._validate_registration_input()
        if not validation_result['valid']:
            self.show_error(validation_result['message'])
            return
            
        # Extract validated data
        full_name = self.full_name_field.text().strip()
        username = self.username_field.text().strip()
        password = self.password_field.text()
        
        try:
            # Check if username is available
            if not self._is_username_available(username):
                self.show_error("Username is already taken")
                return
                
            # Get admin verification
            admin_verification = self._get_admin_verification()
            if not admin_verification['verified']:
                if admin_verification['message']:
                    self.show_error(admin_verification['message'])
                return
                
            # Process the registration
            success = self._process_registration(
                full_name, 
                username, 
                password, 
                admin_verification['admin_id'],
                admin_verification['reason']
            )
            
            if success:
                # Show success message and return to login page
                QtWidgets.QMessageBox.information(
                    self, 
                    "Registration Successful", 
                    f"Staff account for {full_name} has been created successfully."
                )
                self.back_to_login()
                
        except Exception as e:
            error_msg = f"Registration failed: {str(e)}"
            self.show_error(error_msg)
            print(f"Registration error: {e}")  # Consider using proper logging

    def _validate_registration_input(self):
        """Validate all user input fields"""
        full_name = self.full_name_field.text().strip()
        username = self.username_field.text().strip()
        password = self.password_field.text()
        confirm_password = self.confirm_password_field.text()
        
        # Check for empty fields
        if not all([full_name, username, password, confirm_password]):
            return {'valid': False, 'message': "Please fill in all fields"}
        
        # Username validation
        if len(username) < 4:
            return {'valid': False, 'message': "Username must be at least 4 characters"}
            
        # Advanced username validation (alphanumeric and underscores only)
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return {'valid': False, 'message': "Username can only contain letters, numbers, and underscores"}
        
        # Password validation
        if len(password) < 6:
            return {'valid': False, 'message': "Password must be at least 6 characters"}
            
        if password != confirm_password:
            return {'valid': False, 'message': "Passwords do not match"}
        
        return {'valid': True, 'message': ""}

    def _is_username_available(self, username):
        """Check if username is available"""
        conn = DBManager.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
            return existing_user is None
        finally:
            cursor.close()

    def _get_admin_verification(self):
        """Get admin verification for staff account creation"""
        # Create admin verification dialog
        admin_dialog = AdminVerificationDialog(self)
        
        # Show the dialog
        if admin_dialog.exec_() != QtWidgets.QDialog.Accepted:
            return {'verified': False, 'message': ""}
        
        # Get form data
        verification_data = admin_dialog.get_verification_data()
        admin_username = verification_data["admin_username"]
        admin_password = verification_data["admin_password"]
        reason = verification_data["reason"]
        
        # Basic validation
        if not admin_username or not admin_password:
            admin_dialog.reset_fields()  # Reset fields on error
            return {'verified': False, 'message': "Admin credentials are required"}
            
        if not reason:
            admin_dialog.reset_fields()  # Reset fields on error
            return {'verified': False, 'message': "Reason for account creation is required"}
        
        # Verify admin credentials in the database
        from app.utils.auth_manager import AuthManager
        auth_manager = AuthManager()
        admin = auth_manager._auth_strategy.authenticate(admin_username, admin_password)
        
        if not admin or admin.role != 'admin':
            admin_dialog.reset_fields()  # Reset fields on failed verification
            return {'verified': False, 'message': "Invalid admin credentials"}
        
        # Get admin ID
        conn = DBManager.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (admin_username,))
            admin_data = cursor.fetchone()
            admin_id = admin_data['user_id']
            
            # Reset fields after successful verification
            admin_dialog.reset_fields()
            
            return {
                'verified': True, 
                'message': "", 
                'admin_id': admin_id,
                'reason': reason
            }
        finally:
            cursor.close()

    def _process_registration(self, full_name, username, password, admin_id, reason):
        """Process the registration in the database"""
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Insert new user
        conn = DBManager.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "INSERT INTO users (username, password, full_name, role, reason_for_creation, created_by) VALUES (%s, %s, %s, %s, %s, %s)",
                (username, hashed_password, full_name, 'staff', reason, admin_id)
            )
            conn.commit()
            return True
        finally:
            cursor.close()
    
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
        else:
            # If parent reference is lost, create a new login page
            from app.ui.pages.login.login_page import LoginPage
            login_window = LoginPage()
            login_window.show()
        self.close()