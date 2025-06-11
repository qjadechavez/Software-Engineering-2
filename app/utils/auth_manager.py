import hashlib
import os

class AuthManager:
    """Manager for handling user authentication"""
    
    def __init__(self):
        """Initialize the authentication manager"""
        # Demo users for authentication
        self._demo_users = {
            "admin": {
                # Password: "admin123"
                "password_hash": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",
                "salt": "",
                "role": "admin"
            },
            "user": {
                # Password: "user123"
                "password_hash": "cf80cd8aed482d5d1527d7dc72fceff84e6326592848447d2dc0b0e87dfc9a90",
                "salt": "",
                "role": "user"
            }
        }
        
    def authenticate(self, username, password):
        """
        Authenticate a user
        
        Args:
            username (str): Username
            password (str): Password in plain text
            
        Returns:
            dict: User info if authenticated, None otherwise
        """
        # Check if username exists in demo users
        if username in self._demo_users:
            user = self._demo_users[username]
            # Verify password
            if self.generate_password_hash(password, user["salt"]) == user["password_hash"]:
                return {
                    "username": username,
                    "role": user["role"]
                }
        return None
    
    def generate_password_hash(self, password, salt=""):
        """Generate a password hash"""
        return hashlib.sha256((password + salt).encode()).hexdigest()