from PyQt5 import QtCore
from app.utils.auth_manager import AuthManager
from app.utils.db_manager import DBManager

class AuthHandler:
    """Handles authentication related operations for the login page"""
    
    def __init__(self, parent):
        self.parent = parent
        self.auth_manager = AuthManager()
    
    def authenticate(self, username, password):
        """
        Authenticate user with given credentials
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            User object if authentication succeeds, None otherwise
        """
        # Validate input
        if not username or not password:
            self.parent.show_error("Please enter both username and password")
            return None
            
        try:
            # Authenticate user
            user = self.auth_manager.authenticate(username, password)
            
            if not user:
                self.parent.show_error("Invalid username or password")
                return None
                
            return user
            
        except Exception as e:
            self.parent.show_error(f"Login error: Database connection failed")
            print(f"Authentication error: {e}")
            return None
            
    def get_admin_contacts(self):
        """
        Retrieve admin contact information from the database
        
        Returns:
            List of admin users or None if query fails
        """
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Query for admin users
            cursor.execute("SELECT username, full_name, role FROM users WHERE role = 'admin'")
            admins = cursor.fetchall()
            cursor.close()
            
            return admins
        except Exception as e:
            print(f"Error retrieving admin information: {e}")
            return None