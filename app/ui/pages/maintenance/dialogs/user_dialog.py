from PyQt5 import QtWidgets, QtCore
import mysql.connector
from app.utils.db_manager import DBManager
import hashlib
from .base_dialog import BaseDialog

class UserDialog(BaseDialog):
    """Dialog for adding/editing users"""
    
    def __init__(self, parent=None, user=None):
        super(UserDialog, self).__init__(parent, user, "User Management")
        self.user = user
        self.setup_ui()
        
        if user:
            self.populate_fields()
    
    def setup_ui(self):
        """Set up the dialog UI"""
        self.setup_base_ui(650)  # Increased height for security question
        
        # Set dialog title
        if self.user:
            self.header_label.setText("Edit User")
        else:
            self.header_label.setText("Add New User")
        
        # Username field
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setMaxLength(50)
        self.form_layout.addRow("Username:", self.username_input)
        
        # Password field
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setMaxLength(255)
        if self.user:
            self.password_input.setPlaceholderText("Leave blank to keep current password")
        self.form_layout.addRow("Password:", self.password_input)
        
        # Confirm password field
        self.confirm_password_input = QtWidgets.QLineEdit()
        self.confirm_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_input.setMaxLength(255)
        if self.user:
            self.confirm_password_input.setPlaceholderText("Leave blank to keep current password")
        self.form_layout.addRow("Confirm Password:", self.confirm_password_input)
        
        # Full name field
        self.full_name_input = QtWidgets.QLineEdit()
        self.full_name_input.setMaxLength(100)
        self.form_layout.addRow("Full Name:", self.full_name_input)
        
        # Role field
        self.role_combo = QtWidgets.QComboBox()
        self.role_combo.addItems(["staff", "admin"])
        self.form_layout.addRow("Role:", self.role_combo)
        
        # Security question field
        self.security_question_combo = QtWidgets.QComboBox()
        self.security_question_combo.addItems([
            "What is your favorite color?"
        ])
        self.form_layout.addRow("Security Question:", self.security_question_combo)
        
        # Security answer field
        self.security_answer_input = QtWidgets.QLineEdit()
        self.security_answer_input.setMaxLength(255)
        self.security_answer_input.setPlaceholderText("Enter your answer")
        self.form_layout.addRow("Security Answer:", self.security_answer_input)
        
        # Reason for creation (only for new users)
        if not self.user:
            self.reason_input = QtWidgets.QTextEdit()
            self.reason_input.setMaximumHeight(80)
            self.reason_input.setPlaceholderText("Reason for creating this user account...")
            self.form_layout.addRow("Reason:", self.reason_input)
        
        # Connect save button
        self.save_button.clicked.connect(self.save_user)
        
        # Set focus to first field
        self.username_input.setFocus()
        
        # Populate fields if editing
        if self.user:
            self.populate_fields()
    
    def populate_fields(self):
        """Populate form fields with user data"""
        if self.user:
            self.username_input.setText(self.user.get('username', ''))
            self.full_name_input.setText(self.user.get('full_name', ''))
            self.role_combo.setCurrentText(self.user.get('role', 'staff'))
            
            # Set security question if exists
            if self.user.get('security_question'):
                index = self.security_question_combo.findText(self.user.get('security_question'))
                if index >= 0:
                    self.security_question_combo.setCurrentIndex(index)
            
            # Security answer (for editing, show placeholder)
            if self.user.get('security_answer'):
                self.security_answer_input.setPlaceholderText("Leave blank to keep current answer")
    
    def validate_input(self):
        """Validate user input"""
        # Check required fields
        if not self.username_input.text().strip():
            QtWidgets.QMessageBox.warning(self, "Validation Error", "Username is required!")
            return False
        
        if not self.full_name_input.text().strip():
            QtWidgets.QMessageBox.warning(self, "Validation Error", "Full name is required!")
            return False
        
        # Check password for new users
        if not self.user:
            if not self.password_input.text():
                QtWidgets.QMessageBox.warning(self, "Validation Error", "Password is required for new users!")
                return False
        
        # Check password confirmation
        if self.password_input.text() != self.confirm_password_input.text():
            QtWidgets.QMessageBox.warning(self, "Validation Error", "Passwords do not match!")
            return False
        
        # Check password length if provided
        if self.password_input.text() and len(self.password_input.text()) < 3:
            QtWidgets.QMessageBox.warning(self, "Validation Error", "Password must be at least 3 characters long!")
            return False
        
        # Check security question and answer for new users
        if not self.user:
            if not self.security_answer_input.text().strip():
                QtWidgets.QMessageBox.warning(self, "Validation Error", "Security answer is required!")
                return False
        
        return True
    
    def save_user(self):
        """Save user to database"""
        if not self.validate_input():
            return
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor()
            
            username = self.username_input.text().strip()
            full_name = self.full_name_input.text().strip()
            role = self.role_combo.currentText()
            security_question = self.security_question_combo.currentText()
            security_answer = self.security_answer_input.text().strip()
            
            if self.user:
                # Update existing user
                if self.password_input.text():
                    # Update with new password
                    import hashlib
                    password_hash = hashlib.sha256(self.password_input.text().encode()).hexdigest()
                    
                    if security_answer:
                        # Update with security question/answer
                        cursor.execute("""
                            UPDATE users 
                            SET username = %s, password = %s, full_name = %s, role = %s, 
                                security_question = %s, security_answer = %s
                            WHERE user_id = %s
                        """, (username, password_hash, full_name, role, security_question, security_answer, self.user['user_id']))
                    else:
                        # Update without changing security answer
                        cursor.execute("""
                            UPDATE users 
                            SET username = %s, password = %s, full_name = %s, role = %s, 
                                security_question = %s
                            WHERE user_id = %s
                        """, (username, password_hash, full_name, role, security_question, self.user['user_id']))
                else:
                    # Update without changing password
                    if security_answer:
                        # Update with security question/answer
                        cursor.execute("""
                            UPDATE users 
                            SET username = %s, full_name = %s, role = %s, 
                                security_question = %s, security_answer = %s
                            WHERE user_id = %s
                        """, (username, full_name, role, security_question, security_answer, self.user['user_id']))
                    else:
                        # Update without changing security answer
                        cursor.execute("""
                            UPDATE users 
                            SET username = %s, full_name = %s, role = %s, 
                                security_question = %s
                            WHERE user_id = %s
                        """, (username, full_name, role, security_question, self.user['user_id']))
                
                action = "updated"
            else:
                # Check if username already exists
                cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
                if cursor.fetchone():
                    QtWidgets.QMessageBox.warning(self, "Error", "Username already exists!")
                    cursor.close()
                    return
                
                # Insert new user
                import hashlib
                password_hash = hashlib.sha256(self.password_input.text().encode()).hexdigest()
                reason = self.reason_input.toPlainText().strip() if hasattr(self, 'reason_input') else ""
                
                cursor.execute("""
                    INSERT INTO users (username, password, full_name, role, reason_for_creation, security_question, security_answer)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (username, password_hash, full_name, role, reason, security_question, security_answer))
                
                action = "created"
            
            conn.commit()
            cursor.close()
            
            QtWidgets.QMessageBox.information(self, "Success", f"User {action} successfully!")
            self.accept()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save user: {str(e)}")