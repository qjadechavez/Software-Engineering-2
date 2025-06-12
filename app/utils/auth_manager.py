from app.utils.db_manager import DBManager
import mysql.connector

class AuthManager:
    """Manager for handling user authentication using MySQL database"""
    
    def __init__(self):
        """Initialize the authentication manager"""
        pass
        
    def authenticate(self, username, password):
        """
        Authenticate a user against the database
        
        Args:
            username (str): Username
            password (str): Password in plain text
            
        Returns:
            dict: User info if authenticated, None otherwise
        """
        try:
            # Connect to the database using the connection manager
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Query the database for the user - retrieve login_time formatted in 12-hour format
            cursor.execute(
                """SELECT username, role, full_name, 
                   login_time, logout_time, total_session_time,
                   DATE_FORMAT(login_time, '%h:%i %p, %m/%d/%Y') as formatted_login_time,
                   DATE_FORMAT(logout_time, '%h:%i %p, %m/%d/%Y') as formatted_logout_time
                   FROM users WHERE username = %s AND password = %s""",
                (username, password)
            )
            
            user = cursor.fetchone()
            
            # Update the login_time timestamp if user is found
            if user:
                # Get the current time
                import datetime
                current_time = datetime.datetime.now()
                formatted_current_time = current_time.strftime("%I:%M %p, %m/%d/%Y")
                
                # Update login_time to current timestamp
                cursor.execute(
                    "UPDATE users SET login_time = CURRENT_TIMESTAMP() WHERE username = %s",
                    (username,)
                )
                conn.commit()
                
                # Close database connection
                cursor.close()
                conn.close()
                
                print(f"User [{user['username']}] authenticated successfully with role [{user['role']}] and full name [{user['full_name']}] using AuthManager with DBManager")
                
                # Display CURRENT login time instead of previous login time
                print(f"Login recorded @[{formatted_current_time}]\n")
                
                return {
                    "username": user["username"],
                    "role": user["role"], 
                    "full_name": user["full_name"],
                    "login_time": current_time,
                    "formatted_login_time": formatted_current_time,
                    "logout_time": user.get("logout_time"),
                    "formatted_logout_time": user.get("formatted_logout_time"),
                    "total_session_time": user.get("total_session_time", 0)
                }
            
            # Close database connection if user not found
            cursor.close()
            conn.close()
            return None
            
        except mysql.connector.Error as err:
            print(f"Database error during authentication: {err}")
            return None
        
    def logout(self, username):
        """
        Record logout time and update total session time

        Args:
            username (str): Username of the user logging out
    
        Returns:
            dict: Logout information including timestamp and duration
        """
        conn = None
        cursor = None
        
        try:
            # Connect to the database
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get the current login time for calculating session duration
            cursor.execute(
                "SELECT login_time FROM users WHERE username = %s",
                (username,)
            )
            
            user_data = cursor.fetchone()
            if user_data and user_data.get("login_time"):
                login_time = user_data.get("login_time")
                
                # Calculate session duration in seconds
                import datetime
                current_time = datetime.datetime.now()
                session_duration = int((current_time - login_time).total_seconds())
                
                # Format the logout time for display
                formatted_logout = current_time.strftime("%I:%M %p, %m/%d/%Y")
                
                # Update logout time and increment total session time
                cursor.execute(
                    """UPDATE users 
                       SET logout_time = CURRENT_TIMESTAMP(),
                           total_session_time = total_session_time + %s 
                       WHERE username = %s""",
                    (session_duration, username)
                )
                conn.commit()
                
                # Get the updated logout timestamp in the right format
                cursor.execute(
                    """SELECT DATE_FORMAT(logout_time, '%h:%i %p, %m/%d/%Y') as formatted_logout_time 
                       FROM users WHERE username = %s""",
                    (username,)
                )
                formatted_result = cursor.fetchone()
                
                # Print logout information
                print(f"User [{username}] logged out after {session_duration} seconds")
                print(f"Logout recorded @[{formatted_result['formatted_logout_time']}]\n")
                
                # Close database connection
                cursor.close()
                conn.close()
                
                # Return the logout information
                return {
                    "username": username,
                    "logout_time": current_time,
                    "formatted_logout": formatted_result['formatted_logout_time'],
                    "session_duration": session_duration
                }
            
            # Close database connection if user not found
            cursor.close()
            conn.close()
            return None
        
        except mysql.connector.Error as err:
            print(f"Database error during logout: {err}")
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return None