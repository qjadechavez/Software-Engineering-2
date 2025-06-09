import hashlib
import os

class AuthManager:
    """Manager for handling user authentication"""
    
    def __init__(self, db_connection=None):
        """Initialize with optional database connection"""
        self.db_connection = db_connection
        # Demo users (for testing without DB)
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
        if self.db_connection:
            # Use database authentication when DB is available
            return self._db_authenticate(username, password)
        else:
            # Use demo authentication for testing
            return self._demo_authenticate(username, password)
    
    def _demo_authenticate(self, username, password):
        """Demo authentication for testing without DB"""
        if username in self._demo_users:
            user = self._demo_users[username]
            # Hash the provided password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            if password_hash == user["password_hash"]:
                return {
                    "username": username,
                    "role": user["role"]
                }
        return None
    
    def _db_authenticate(self, username, password):
        """Real authentication using database"""
        if not self.db_connection:
            return None
            
        # Implementation would depend on your database structure
        # Example:
        # cursor = self.db_connection.cursor()
        # cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        # user = cursor.fetchone()
        # if user:
        #     stored_hash = user["password_hash"]
        #     salt = user["salt"]
        #     password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        #     if password_hash == stored_hash:
        #         return {"username": username, "role": user["role"]}
        return None
    
    def generate_password_hash(self, password, salt=""):
        """Generate a password hash"""
        return hashlib.sha256((password + salt).encode()).hexdigest()