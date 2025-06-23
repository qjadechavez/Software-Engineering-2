from PyQt5 import QtWidgets, QtGui, QtCore

class AdminVerificationDialog(QtWidgets.QDialog):
    """Dialog for admin verification when creating a new staff account"""
    
    def __init__(self, parent=None):
        super(AdminVerificationDialog, self).__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the admin verification dialog UI"""
        self.setWindowTitle("Admin Verification")
        self.setFixedSize(400, 300)
        
        # Dialog layout
        layout = QtWidgets.QVBoxLayout(self)
        
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
        self.admin_username_field = QtWidgets.QLineEdit()
        self.admin_username_field.setObjectName("admin_username")
        self.admin_username_field.setPlaceholderText("Admin username")
        form_layout.addRow("Admin Username:", self.admin_username_field)
        
        # Admin password
        self.admin_password_field = QtWidgets.QLineEdit()
        self.admin_password_field.setObjectName("admin_password")
        self.admin_password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.admin_password_field.setPlaceholderText("Admin password")
        form_layout.addRow("Admin Password:", self.admin_password_field)
        
        # Reason for creation
        self.reason_field = QtWidgets.QTextEdit()
        self.reason_field.setObjectName("reason")
        self.reason_field.setPlaceholderText("Enter the reason for creating this account")
        self.reason_field.setMaximumHeight(80)
        form_layout.addRow("Reason:", self.reason_field)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def get_verification_data(self):
        """Get the entered verification data"""
        return {
            "admin_username": self.admin_username_field.text().strip(),
            "admin_password": self.admin_password_field.text(),
            "reason": self.reason_field.toPlainText().strip()
        }