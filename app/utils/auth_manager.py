from app.utils.db_manager import DBManager
import mysql.connector
import datetime
from abc import ABC, abstractmethod

class UserSession:
    """Class representing a user's authentication session"""
    
    def __init__(self, user_data):
        """Initialize a user session with user data
        
        Args:
            user_data (dict): User information from database
        """
        self.user_id = user_data.get("user_id")
        self.username = user_data.get("username")
        self.role = user_data.get("role")
        self.full_name = user_data.get("full_name")
        self.login_time = datetime.datetime.now()
        self.logout_time = None
        self.formatted_login_time = self.login_time.strftime("%I:%M %p, %m/%d/%Y")
        self.total_session_time = user_data.get("total_session_time", 0)
    
    def to_dict(self):
        """Convert session to dictionary for passing to UI
        
        Returns:
            dict: Session information
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role,
            "full_name": self.full_name,
            "login_time": self.login_time,
            "formatted_login_time": self.formatted_login_time,
            "logout_time": self.logout_time,
            "total_session_time": self.total_session_time
        }
    
    def end_session(self):
        """End the current session and calculate duration
        
        Returns:
            int: Session duration in seconds
        """
        self.logout_time = datetime.datetime.now()
        session_duration = int((self.logout_time - self.login_time).total_seconds())
        self.total_session_time += session_duration
        return session_duration
    
    def get_logout_info(self):
        """Get information about the logout with formatted session duration
        
        Returns:
            dict: Logout information with duration in minutes and seconds format
        """
        if not self.logout_time:
            return None
            
        formatted_logout = self.logout_time.strftime("%I:%M %p, %m/%d/%Y")
        
        # Calculate session duration in seconds
        session_seconds = int((self.logout_time - self.login_time).total_seconds())
        
        # Format duration as minutes and seconds
        minutes = session_seconds // 60
        remaining_seconds = session_seconds % 60
        formatted_duration = f"{minutes} min {remaining_seconds} sec"
        
        return {
            "username": self.username,
            "logout_time": self.logout_time,
            "formatted_logout": formatted_logout,
            "session_duration": session_seconds, 
            "formatted_duration": formatted_duration
        }


class IAuthStrategy(ABC):
    """Abstract interface for authentication strategies"""
    
    @abstractmethod
    def authenticate(self, username, credential):
        """Authenticate a user
        
        Args:
            username (str): Username
            credential: Credential for authentication
            
        Returns:
            UserSession: Session if authenticated, None otherwise
        """
        pass


class DatabaseAuthStrategy(IAuthStrategy):
    """Database authentication implementation"""
    
    def authenticate(self, username, password):
        """Authenticate user against database
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            UserSession: Session if authenticated, None otherwise
        """
        conn = None
        cursor = None
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                """SELECT user_id, username, role, full_name, 
                   login_time, logout_time, total_session_time
                   FROM users WHERE username = %s AND password = %s""",
                (username, password)
            )
            
            user = cursor.fetchone()
            if not user:
                return None
                
            # Create user session
            return UserSession(user)
            
        except mysql.connector.Error as err:
            print(f"Authentication error: {err}")
            return None
            
        finally:
            if cursor:
                cursor.close()


class AuthEventLogger:
    """Logger for authentication events"""
    
    @staticmethod
    def log_login(session):
        """Log successful login
        
        Args:
            session (UserSession): User session
        """
        print(f"User [{session.username}] authenticated successfully")
        print(f"Login recorded @[{session.formatted_login_time}]")
    
    @staticmethod
    def log_logout(username, logout_info):
        """Log successful logout
        
        Args:
            username (str): Username
            logout_info (dict): Logout information
        """
        print(f"User [{username}] logged out after {logout_info['formatted_duration']}")
        print(f"Logout recorded @[{logout_info['formatted_logout']}]")
    
    @staticmethod
    def log_error(message):
        """Log authentication error
        
        Args:
            message (str): Error message
        """
        print(f"Authentication error: {message}")


class SessionRepository:
    """Repository for managing user sessions in database"""
    
    @staticmethod
    def update_login(session):
        """Update login time in database
        
        Args:
            session (UserSession): User session to update
            
        Returns:
            bool: True if successful, False otherwise
        """
        conn = None
        cursor = None
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor()
            
            # Update login_time
            cursor.execute(
                "UPDATE users SET login_time = %s WHERE user_id = %s",
                (session.login_time, session.user_id)
            )
            conn.commit()
            return True
            
        except mysql.connector.Error as err:
            print(f"Database error updating login: {err}")
            return False
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.commit()
    
    @staticmethod
    def update_logout(username, session_duration):
        """Update logout time and session duration in database
        
        Args:
            username (str): Username to update
            session_duration (int): Session duration in seconds
            
        Returns:
            bool: True if successful, False otherwise
        """
        conn = None
        cursor = None
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor()
            
            # Update logout time and session time
            cursor.execute(
                """UPDATE users 
                   SET logout_time = CURRENT_TIMESTAMP(),
                       total_session_time = total_session_time + %s 
                   WHERE username = %s""",
                (session_duration, username)
            )
            conn.commit()
            return True
            
        except mysql.connector.Error as err:
            print(f"Database error updating logout: {err}")
            return False
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.commit()


class AuthManager:
    """Manager for handling user authentication with advanced OOP patterns"""
    
    # Singleton instance
    _instance = None
    
    # Default auth strategy
    _auth_strategy = DatabaseAuthStrategy()
    
    # Active user sessions (username -> UserSession)
    _active_sessions = {}
    
    def __new__(cls):
        """Create a new instance or return existing one (Singleton pattern)"""
        if cls._instance is None:
            cls._instance = super(AuthManager, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def set_auth_strategy(cls, strategy):
        """Set the authentication strategy (Strategy pattern)
        
        Args:
            strategy (IAuthStrategy): Authentication strategy to use
        """
        cls._auth_strategy = strategy
    
    def authenticate(self, username, password):
        """Authenticate a user
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            dict: User info if authenticated, None otherwise
        """
        # Use current strategy to authenticate
        user_session = self._auth_strategy.authenticate(username, password)
        
        if user_session:
            # Store active session
            self._active_sessions[username] = user_session
            
            # Update login time in database
            SessionRepository.update_login(user_session)
            
            # Log the event
            AuthEventLogger.log_login(user_session)
            
            # Return user information
            return user_session.to_dict()
        
        return None
    
    def logout(self, username):
        """Record logout time and update session time
        
        Args:
            username (str): Username of the user logging out
        
        Returns:
            dict: Logout information or None if failed
        """
        # Get active session
        user_session = self._active_sessions.get(username)
        if not user_session:
            return None
        
        try:
            # End the session
            session_duration = user_session.end_session()
            
            # Update logout time in database
            SessionRepository.update_logout(username, session_duration)
            
            # Get logout information
            logout_info = user_session.get_logout_info()
            
            # Log the event
            AuthEventLogger.log_logout(username, logout_info)
            
            # Remove from active sessions
            self._active_sessions.pop(username, None)
            
            return logout_info
            
        except Exception as err:
            AuthEventLogger.log_error(str(err))
            return None
    
    def get_active_session(self, username):
        """Get active session for a user
        
        Args:
            username (str): Username
            
        Returns:
            UserSession: User session or None
        """
        return self._active_sessions.get(username)