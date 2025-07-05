from PyQt5 import QtWidgets, QtGui, QtCore
from app.utils.db_manager import DBManager
import hashlib

class ForgotPasswordDialog(QtWidgets.QDialog):
    """Dialog for password recovery using security questions"""
    
    def __init__(self, parent=None):
        super(ForgotPasswordDialog, self).__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the dialog UI"""
        self.setWindowTitle("Forgot Password")
        self.setFixedSize(450, 400)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333;
                font-size: 12px;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #007ACC;
            }
            QPushButton {
                background-color: #007ACC;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004578;
            }
        """)
        
        # Main layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QtWidgets.QLabel("Password Recovery")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #007ACC;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QtWidgets.QLabel("Enter your username and answer your security question to reset your password.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(desc)
        
        # Form layout
        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(10)
        
        # Username field
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.textChanged.connect(self.load_security_question)
        form_layout.addRow("Username:", self.username_input)
        
        # Security question display
        self.security_question_label = QtWidgets.QLabel("Security question will appear here")
        self.security_question_label.setStyleSheet("color: #666; font-style: italic; padding: 8px; background-color: #f9f9f9; border-radius: 4px;")
        self.security_question_label.setWordWrap(True)
        form_layout.addRow("Security Question:", self.security_question_label)
        
        # Security answer field
        self.security_answer_input = QtWidgets.QLineEdit()
        self.security_answer_input.setPlaceholderText("Enter your answer")
        self.security_answer_input.setEnabled(False)
        form_layout.addRow("Answer:", self.security_answer_input)
        
        # New password field
        self.new_password_input = QtWidgets.QLineEdit()
        self.new_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.new_password_input.setPlaceholderText("Enter new password")
        self.new_password_input.setEnabled(False)
        form_layout.addRow("New Password:", self.new_password_input)
        
        # Confirm password field
        self.confirm_password_input = QtWidgets.QLineEdit()
        self.confirm_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("Confirm new password")
        self.confirm_password_input.setEnabled(False)
        form_layout.addRow("Confirm Password:", self.confirm_password_input)
        
        layout.addLayout(form_layout)
        
        # Error message
        self.error_label = QtWidgets.QLabel()
        self.error_label.setStyleSheet("color: #d32f2f; font-weight: bold;")
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        self.error_label.hide()
        layout.addWidget(self.error_label)
        
        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setStyleSheet("background-color: #666;")
        self.cancel_button.clicked.connect(self.reject)
        
        self.reset_button = QtWidgets.QPushButton("Reset Password")
        self.reset_button.setEnabled(False)
        self.reset_button.clicked.connect(self.reset_password)
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.reset_button)
        
        layout.addLayout(button_layout)
        
    def load_security_question(self):
        """Load security question for the entered username"""
        username = self.username_input.text().strip()
        if not username:
            self.security_question_label.setText("Security question will appear here")
            self.security_answer_input.setEnabled(False)
            self.new_password_input.setEnabled(False)
            self.confirm_password_input.setEnabled(False)
            self.reset_button.setEnabled(False)
            return
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT security_question FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            cursor.close()
            
            if result and result['security_question']:
                # Since we only have one question, we can display it directly
                self.security_question_label.setText("What is your favorite color?")
                self.security_answer_input.setEnabled(True)
                self.new_password_input.setEnabled(True)
                self.confirm_password_input.setEnabled(True)
                self.reset_button.setEnabled(True)
                self.hide_error()
            else:
                self.security_question_label.setText("User not found or no security question set")
                self.security_answer_input.setEnabled(False)
                self.new_password_input.setEnabled(False)
                self.confirm_password_input.setEnabled(False)
                self.reset_button.setEnabled(False)
                
        except Exception as e:
            self.show_error("Database error occurred")
            print(f"Error loading security question: {e}")
    
    def reset_password(self):
        """Reset the user's password with enhanced validation"""
        username = self.username_input.text().strip()
        answer = self.security_answer_input.text().strip()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        # Validate inputs
        if not all([username, answer, new_password, confirm_password]):
            self.show_error("All fields are required")
            return
        
        if new_password != confirm_password:
            self.show_error("Passwords do not match")
            return
        
        if len(new_password) < 6:
            self.show_error("Password must be at least 6 characters long")
            return
        
        # Validate security answer format
        if len(answer) < 2:
            self.show_error("Security answer must be at least 2 characters long")
            return
        
        if answer.isdigit():
            self.show_error("Security answer cannot be only numbers")
            return
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Verify security answer (case-insensitive)
            cursor.execute("SELECT security_answer FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            
            if not result:
                self.show_error("User not found")
                cursor.close()
                return
            
            # Compare answers in lowercase for case-insensitive matching
            stored_answer = result['security_answer'].lower() if result['security_answer'] else ""
            provided_answer = answer.lower()
            
            if stored_answer != provided_answer:
                self.show_error("Incorrect security answer")
                cursor.close()
                return
            
            # Update password
            import hashlib
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            cursor.execute("UPDATE users SET password = %s WHERE username = %s", (hashed_password, username))
            conn.commit()
            cursor.close()
            
            QtWidgets.QMessageBox.information(self, "Success", "Password reset successfully!")
            self.accept()
            
        except Exception as e:
            self.show_error("Failed to reset password")
            print(f"Error resetting password: {e}")
    
    def show_error(self, message):
        """Show error message"""
        self.error_label.setText(message)
        self.error_label.show()
        
    def hide_error(self):
        """Hide error message"""
        self.error_label.hide()