from app.utils.auth_manager import AuthManager
from app.utils.db_manager import DBManager
import hashlib

class RegisterAuthHandler:
    """Handles authentication-related operations for the register page"""
    
    def __init__(self, parent):
        self.parent = parent
        self.auth_manager = AuthManager()
    
    def check_username_availability(self, username):
        """
        Check if username is available in the database
        
        Args:
            username: Username to check
            
        Returns:
            bool: True if available, False if taken
        """
        conn = DBManager.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
            return existing_user is None
        finally:
            cursor.close()
    
    def verify_admin_credentials(self, admin_username, admin_password, reason):
        """
        Verify that provided credentials belong to an admin
        
        Args:
            admin_username: Admin username
            admin_password: Admin password
            reason: Reason for account creation
            
        Returns:
            dict: Verification result with status, message, admin_id if successful
        """
        # Basic validation
        if not admin_username or not admin_password:
            return {'verified': False, 'message': "Admin credentials are required"}
            
        if not reason:
            return {'verified': False, 'message': "Reason for account creation is required"}
        
        # Verify admin credentials in the database
        admin = self.auth_manager._auth_strategy.authenticate(admin_username, admin_password)
        
        if not admin or admin.role != 'admin':
            return {'verified': False, 'message': "Invalid admin credentials"}
        
        # Get admin ID
        conn = DBManager.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (admin_username,))
            admin_data = cursor.fetchone()
            admin_id = admin_data['user_id']
            return {
                'verified': True, 
                'message': "", 
                'admin_id': admin_id,
                'reason': reason
            }
        finally:
            cursor.close()
    
    def create_staff_account(self, full_name, username, password, admin_id, reason):
        """
        Create a new staff account in the database
        
        Args:
            full_name: User's full name
            username: Username
            password: Password (plain text)
            admin_id: ID of admin creating the account
            reason: Reason for account creation
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
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
        except Exception as e:
            print(f"Account creation error: {e}")
            return False
    
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