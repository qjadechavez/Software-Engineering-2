class AuthManager:
    """Manager for handling user authentication"""
    
    def __init__(self):
        """Initialize the authentication manager"""
        # User accounts
        self._users = {
            "juan": {
                "password": "juan123",
                "role": "admin"
            },
            "maria": {
                "password": "maria123",
                "role": "staff"
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
        # Check if username exists in users
        if username in self._users:
            user = self._users[username]
            # Verify password (plain text comparison)
            if password == user["password"]:
                print(f"User {username} authenticated successfully.")
                return {
                    "username": username,
                    "role": user["role"]
                }
        return None