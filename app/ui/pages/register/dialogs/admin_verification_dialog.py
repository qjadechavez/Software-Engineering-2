from PyQt5 import QtWidgets, QtGui, QtCore
from app.ui.pages.inventory.dialogs.base_dialog import BaseDialog

class AdminVerificationDialog(BaseDialog):
    """Dialog for admin verification when creating a new staff account"""
    
    def __init__(self, parent=None):
        super(AdminVerificationDialog, self).__init__(parent, None, "Admin Verification")
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the admin verification dialog UI"""
        self.setup_base_ui(500)  # Reduced height since we removed combo box
        
        self.header_label.setText("Admin Verification Required")
        
        # Description
        desc_label = QtWidgets.QLabel("Please enter admin credentials to continue with staff registration:")
        desc_label.setWordWrap(True)
        self.form_layout.addRow(desc_label)
        
        # Admin username
        self.admin_username_field = QtWidgets.QLineEdit()
        self.admin_username_field.setObjectName("admin_username")
        self.admin_username_field.setPlaceholderText("Admin username")
        self.form_layout.addRow("Admin Username:", self.admin_username_field)
        
        # Admin password
        self.admin_password_field = QtWidgets.QLineEdit()
        self.admin_password_field.setObjectName("admin_password")
        self.admin_password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.admin_password_field.setPlaceholderText("Admin password")
        self.form_layout.addRow("Admin Password:", self.admin_password_field)
        
        # Security Question Display (read-only)
        security_question_display = QtWidgets.QLabel("What is your favorite color?")
        security_question_display.setStyleSheet("""
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            padding: 8px;
            border-radius: 4px;
            color: #333;
        """)
        self.form_layout.addRow("Security Question:", security_question_display)
        
        # Security answer for new user
        self.security_answer_field = QtWidgets.QLineEdit()
        self.security_answer_field.setPlaceholderText("Enter your favorite color")
        self.form_layout.addRow("Security Answer:", self.security_answer_field)
        
        # Reason for creation
        self.reason_field = QtWidgets.QTextEdit()
        self.reason_field.setObjectName("reason")
        self.reason_field.setPlaceholderText("Enter the reason for creating this account")
        self.reason_field.setMaximumHeight(80)
        self.form_layout.addRow("Reason:", self.reason_field)
        
        # Update save button
        self.save_button.setText("Verify")
        self.save_button.clicked.connect(self.verify_admin)
    
    def verify_admin(self):
        """Verify admin credentials"""
        admin_username = self.admin_username_field.text().strip()
        admin_password = self.admin_password_field.text().strip()
        security_answer = self.security_answer_field.text().strip()
        reason = self.reason_field.toPlainText().strip()
        
        if not admin_username or not admin_password or not security_answer or not reason:
            QtWidgets.QMessageBox.warning(self, "Warning", "All fields are required.")
            return
        
        # Accept the dialog first
        self.accept()
    
    def reset_fields(self):
        """Reset all input fields"""
        self.admin_username_field.clear()
        self.admin_password_field.clear()
        self.security_answer_field.clear()
        self.reason_field.clear()
    
    def get_verification_data(self):
        """Get the entered verification data"""
        return {
            "admin_username": self.admin_username_field.text().strip(),
            "admin_password": self.admin_password_field.text(),
            "security_question": "What is your favorite color?",
            "security_answer": self.security_answer_field.text().strip(),
            "reason": self.reason_field.toPlainText().strip()
        }