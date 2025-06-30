from PyQt5 import QtWidgets, QtCore, QtGui
import mysql.connector
from app.utils.db_manager import DBManager
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
from ..style_factory import StyleFactory
from ..table_factory import TableFactory
from ..control_panel_factory import ControlPanelFactory
from ..dialogs import UserDialog

# Set matplotlib to use a non-GUI backend
matplotlib.use('Qt5Agg')

class UserManagementTab(QtWidgets.QWidget):
    """Tab for user management and statistics"""
    
    def __init__(self, parent=None):
        super(UserManagementTab, self).__init__()
        self.parent = parent
        
        # Check if parent has user info and validate access
        if self.parent and hasattr(self.parent, 'user_info'):
            user_role = self.parent.user_info.get("role", "").lower()
            if user_role != "admin":
                self.show_access_denied()
                return
        
        self.setup_ui()
        self.load_user_data()
    
    def show_access_denied(self):
        """Show access denied message in the tab"""
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        message = QtWidgets.QLabel("Access denied. Admin privileges required.")
        message.setStyleSheet("color: #f44336; font-size: 16px; font-weight: bold;")
        message.setAlignment(QtCore.Qt.AlignCenter)
        
        layout.addWidget(message)
    
    def setup_ui(self):
        """Set up the UI components for the user management tab"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 15, 10, 10)
        self.layout.setSpacing(15)
        
        # Header section
        header_layout = QtWidgets.QVBoxLayout()
        
        title_label = QtWidgets.QLabel("User Management")
        title_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        desc_label = QtWidgets.QLabel("Manage system users and view user statistics")
        desc_label.setStyleSheet("color: #cccccc; font-size: 12px;")
        header_layout.addWidget(desc_label)
        
        self.layout.addLayout(header_layout)
        
        # Statistics and chart section - reduced height
        stats_layout = QtWidgets.QHBoxLayout()
        stats_layout.setSpacing(15)
        
        # Statistics cards
        stats_cards_layout = QtWidgets.QVBoxLayout()
        stats_cards_layout.setSpacing(10)
        
        self.total_users_card = self.create_info_card("Total Users", "0", "#4CAF50", "users")
        self.admin_users_card = self.create_info_card("Admin Users", "0", "#FF9800", "admin")
        self.staff_users_card = self.create_info_card("Staff Users", "0", "#2196F3", "staff")
        
        stats_cards_layout.addWidget(self.total_users_card)
        stats_cards_layout.addWidget(self.admin_users_card)
        stats_cards_layout.addWidget(self.staff_users_card)
        stats_cards_layout.addStretch()
        
        # Pie chart - smaller size
        chart_frame = QtWidgets.QFrame()
        chart_frame.setFixedHeight(250)  # Fixed smaller height
        chart_frame.setStyleSheet("""
            QFrame {
                background-color: #232323;
                border-radius: 8px;
                border: 1px solid rgba(100, 100, 100, 0.3);
            }
        """)
        chart_layout = QtWidgets.QVBoxLayout(chart_frame)
        chart_layout.setContentsMargins(15, 15, 15, 15)
        
        chart_title = QtWidgets.QLabel("User Distribution")
        chart_title.setStyleSheet("color: white; font-size: 14px; font-weight: bold; border: none; background: transparent;")
        chart_layout.addWidget(chart_title)
        
        # Create matplotlib figure - smaller size
        self.figure = Figure(figsize=(4, 3), facecolor='#232323')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: #232323;")
        chart_layout.addWidget(self.canvas)
        
        stats_layout.addLayout(stats_cards_layout, 1)
        stats_layout.addWidget(chart_frame, 1)  # Reduced proportion
        
        # Add stats section with reduced stretch factor
        stats_container = QtWidgets.QWidget()
        stats_container.setLayout(stats_layout)
        stats_container.setMaximumHeight(300)  # Limit maximum height
        self.layout.addWidget(stats_container)
        
        # User management section - more space allocated
        management_frame = QtWidgets.QFrame()
        management_frame.setStyleSheet("""
            QFrame {
                background-color: #232323;
                border-radius: 8px;
                border: 1px solid rgba(100, 100, 100, 0.3);
            }
        """)
        management_layout = QtWidgets.QVBoxLayout(management_frame)
        management_layout.setContentsMargins(20, 20, 20, 20)
        management_layout.setSpacing(15)
        
        # Management header
        mgmt_title = QtWidgets.QLabel("User Management")
        mgmt_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold; border: none;")
        management_layout.addWidget(mgmt_title)
        
        # Search and controls
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search users...")
        
        self.control_layout = ControlPanelFactory.create_search_control(
            self.search_input,
            "+ Add User",
            self.show_add_user_dialog,
            self.filter_users
        )
        management_layout.addLayout(self.control_layout)
        
        # Users table
        self.users_table = TableFactory.create_table()
        
        # Define column headers - replaced Status with Created Date
        user_columns = [
            ("ID", 0.08),
            ("Username", 0.20),
            ("Full Name", 0.25),
            ("Role", 0.15),
            ("Last Login", 0.20),
            ("Created Date", 0.12)  # Changed from Status to Created Date
        ]
        
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.users_table, user_columns, screen_width)
        
        # Add context menu
        self.users_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.users_table.customContextMenuRequested.connect(self.show_context_menu)
        
        management_layout.addWidget(self.users_table)
        
        # Give more space to management frame
        self.layout.addWidget(management_frame, 3)  # Increased stretch factor from 1 to 3
    
    def create_info_card(self, title, value, color, icon_type):
        """Create an information card widget"""
        card = QtWidgets.QFrame()
        card.setFixedHeight(80)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #2a2a2a;
                border-radius: 8px;
                border: 1px solid rgba(100, 100, 100, 0.3);
            }}
        """)
        
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)
        
        # Icon
        icon_label = QtWidgets.QLabel()
        icon_label.setFixedSize(32, 32)
        icon_label.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        
        # Set icon based on type
        icon_map = {
            "users": "👥",
            "admin": "👑",
            "staff": "👤",
            "sessions": "🔗"
        }
        icon_label.setText(icon_map.get(icon_type, "👤"))
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        
        # Text content
        text_layout = QtWidgets.QVBoxLayout()
        text_layout.setSpacing(2)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("color: #cccccc; font-size: 12px; border: none; background: transparent;")
        
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-size: 18px; font-weight: bold; border: none; background: transparent;")
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        
        layout.addWidget(icon_label)
        layout.addLayout(text_layout)
        layout.addStretch()
        
        # Store reference to value label for updates
        card.value_label = value_label
        
        return card
    
    def create_pie_chart(self, admin_count, staff_count):
        """Create pie chart for user distribution"""
        self.figure.clear()
        
        if admin_count == 0 and staff_count == 0:
            # Show empty chart message
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No Users Found', ha='center', va='center', 
                   fontsize=16, color='white', transform=ax.transAxes)
            ax.set_facecolor('#232323')
            ax.axis('off')
        else:
            ax = self.figure.add_subplot(111)
            
            # Data for pie chart
            sizes = [admin_count, staff_count]
            labels = ['Admin', 'Staff']
            colors = ['#FF9800', '#2196F3']
            
            # Create pie chart
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, 
                                            autopct='%1.1f%%', startangle=90,
                                            textprops={'color': 'white', 'fontsize': 12})
            
            # Styling
            ax.set_facecolor('#232323')
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        
        self.canvas.draw()
    
    def load_user_data(self):
        """Load user data from database"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get all users
            cursor.execute("""
                SELECT user_id, username, full_name, role, login_time, 
                       logout_time, created_at
                FROM users 
                ORDER BY created_at DESC
            """)
            users = cursor.fetchall()
            
            # Count users by role
            admin_count = sum(1 for user in users if user['role'] == 'admin')
            staff_count = sum(1 for user in users if user['role'] == 'staff')
            total_count = len(users)
            
            # Update info cards
            self.total_users_card.value_label.setText(str(total_count))
            self.admin_users_card.value_label.setText(str(admin_count))
            self.staff_users_card.value_label.setText(str(staff_count))
            
            # Update pie chart
            self.create_pie_chart(admin_count, staff_count)
            
            # Populate users table
            self.users_table.setRowCount(len(users))
            
            for row, user in enumerate(users):
                # ID
                id_item = QtWidgets.QTableWidgetItem(str(user['user_id']))
                id_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.users_table.setItem(row, 0, id_item)
                
                # Username
                self.users_table.setItem(row, 1, QtWidgets.QTableWidgetItem(user['username']))
                
                # Full Name
                self.users_table.setItem(row, 2, QtWidgets.QTableWidgetItem(user['full_name']))
                
                # Role
                role_item = QtWidgets.QTableWidgetItem(user['role'].title())
                role_item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                # Color code roles
                if user['role'] == 'admin':
                    role_item.setForeground(QtGui.QColor("#FF9800"))
                else:
                    role_item.setForeground(QtGui.QColor("#2196F3"))
                
                self.users_table.setItem(row, 3, role_item)
                
                # Last Login
                login_time = user['login_time']
                login_str = login_time.strftime('%Y-%m-%d %H:%M') if login_time else "Never"
                login_item = QtWidgets.QTableWidgetItem(login_str)
                login_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.users_table.setItem(row, 4, login_item)
                
                # Created Date - replaced Status column
                created_at = user['created_at']
                created_str = created_at.strftime('%Y-%m-%d %H:%M') if created_at else "Unknown"
                created_item = QtWidgets.QTableWidgetItem(created_str)
                created_item.setTextAlignment(QtCore.Qt.AlignCenter)
                created_item.setForeground(QtGui.QColor("#B0B0B0"))  # Gray color for created date
                self.users_table.setItem(row, 5, created_item)
            
            cursor.close()
            
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def filter_users(self):
        """Filter users based on search input"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.users_table.rowCount()):
            show_row = False
            
            # Check username, full name, and role columns
            for col in [1, 2, 3]:  # Username, Full Name, Role columns
                item = self.users_table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            
            self.users_table.setRowHidden(row, not show_row)
    
    def show_context_menu(self, position):
        """Show context menu for user actions"""
        item = self.users_table.itemAt(position)
        if item is None:
            return
        
        row = item.row()
        user_id = int(self.users_table.item(row, 0).text())
        username = self.users_table.item(row, 1).text()
        
        menu = QtWidgets.QMenu(self)
        
        edit_action = menu.addAction("Edit User")
        edit_action.triggered.connect(lambda: self.edit_user(row))
        
        reset_password_action = menu.addAction("Reset Password")
        reset_password_action.triggered.connect(lambda: self.reset_user_password(row))
        
        menu.addSeparator()
        
        delete_action = menu.addAction("Delete User")
        delete_action.triggered.connect(lambda: self.delete_user(row))
        
        # Don't allow deleting the current user (assuming user_id 1 is admin)
        if user_id == 1:
            delete_action.setEnabled(False)
            delete_action.setText("Delete User (Protected)")
        
        menu.exec_(self.users_table.mapToGlobal(position))
    
    def show_add_user_dialog(self):
        """Show dialog to add a new user"""
        dialog = UserDialog(self.parent or self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.load_user_data()
    
    def edit_user(self, row):
        """Edit the selected user"""
        user_id = int(self.users_table.item(row, 0).text())
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            
            if user:
                dialog = UserDialog(self.parent or self, user)
                if dialog.exec_() == QtWidgets.QDialog.Accepted:
                    self.load_user_data()
            
            cursor.close()
            
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def delete_user(self, row):
        """Delete the selected user"""
        user_id = int(self.users_table.item(row, 0).text())
        username = self.users_table.item(row, 1).text()
        
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete user '{username}'?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                conn = DBManager.get_connection()
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                conn.commit()
                cursor.close()
                
                QtWidgets.QMessageBox.information(self, "Success", f"User '{username}' deleted successfully!")
                self.load_user_data()
                
            except mysql.connector.Error as err:
                if self.parent:
                    self.parent.show_error_message(f"Database error: {err}")
                else:
                    QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def reset_user_password(self, row):
        """Reset password for the selected user"""
        user_id = int(self.users_table.item(row, 0).text())
        username = self.users_table.item(row, 1).text()
        
        # Create password reset dialog
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Reset Password")
        dialog.setFixedWidth(400)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #2a2a2a;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #444;
                background-color: #333;
                color: white;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton#cancelButton {
                background-color: #555;
            }
            QPushButton#cancelButton:hover {
                background-color: #666;
            }
        """)
        
        # Create layout
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QtWidgets.QLabel(f"Reset Password for {username}")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Description
        description = QtWidgets.QLabel("Enter a new password below:")
        layout.addWidget(description)
        
        # New password field
        new_password_layout = QtWidgets.QFormLayout()
        new_password_input = QtWidgets.QLineEdit()
        new_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        new_password_input.setPlaceholderText("Enter new password")
        new_password_layout.addRow("New Password:", new_password_input)
        
        # Confirm password field
        confirm_password_input = QtWidgets.QLineEdit()
        confirm_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        confirm_password_input.setPlaceholderText("Confirm new password")
        new_password_layout.addRow("Confirm Password:", confirm_password_input)
        
        layout.addLayout(new_password_layout)
        
        # Error message (hidden initially)
        error_label = QtWidgets.QLabel("")
        error_label.setStyleSheet("color: #f44336;")
        error_label.setVisible(False)
        layout.addWidget(error_label)
        
        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        
        reset_button = QtWidgets.QPushButton("Reset Password")
        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.setObjectName("cancelButton")
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(reset_button)
        
        layout.addLayout(button_layout)
        
        # Button actions
        cancel_button.clicked.connect(dialog.reject)
        
        def validate_and_reset():
            new_password = new_password_input.text()
            confirm_password = confirm_password_input.text()
            
            # Validate passwords
            if not new_password:
                error_label.setText("Password cannot be empty")
                error_label.setVisible(True)
                return
                
            if new_password != confirm_password:
                error_label.setText("Passwords do not match")
                error_label.setVisible(True)
                return
                
            if len(new_password) < 3:
                error_label.setText("Password must be at least 3 characters")
                error_label.setVisible(True)
                return
            
            # Reset password
            try:
                conn = DBManager.get_connection()
                cursor = conn.cursor()
                
                # Hash the password
                import hashlib
                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                
                # Update password in database
                cursor.execute(
                    "UPDATE users SET password = %s WHERE user_id = %s",
                    (hashed_password, user_id)
                )
                conn.commit()
                cursor.close()
                
                QtWidgets.QMessageBox.information(
                    dialog,
                    "Success",
                    f"Password for '{username}' has been reset successfully!"
                )
                dialog.accept()
                
            except mysql.connector.Error as err:
                error_label.setText(f"Database error: {err}")
                error_label.setVisible(True)
        
        reset_button.clicked.connect(validate_and_reset)
        
        # Show dialog
        dialog.exec_()
    
    def refresh_data(self):
        """Refresh user data"""
        self.load_user_data()