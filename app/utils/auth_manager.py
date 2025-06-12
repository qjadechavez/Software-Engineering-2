from app.utils.db_manager import DBManager
import mysql.connector
import datetime

class AuthManager:
    """Manager for handling user authentication with improved security and error handling"""
    
    def authenticate(self, username, password):
        """
        Authenticate a user against the database
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            dict: User info if authenticated, None otherwise
        """
        conn = None
        cursor = None
        
        try:
            # Connect to the database
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Query the database for the user
            # In a real application, passwords should be hashed!
            cursor.execute(
                """SELECT user_id, username, role, full_name, 
                   login_time, logout_time, total_session_time
                   FROM users WHERE username = %s AND password = %s""",
                (username, password)
            )
            
            user = cursor.fetchone()
            
            # Update login timestamp if user is found
            if user:
                current_time = datetime.datetime.now()
                formatted_time = current_time.strftime("%I:%M %p, %m/%d/%Y")
                
                # Update login_time
                cursor.execute(
                    "UPDATE users SET login_time = CURRENT_TIMESTAMP() WHERE user_id = %s",
                    (user['user_id'],)
                )
                conn.commit()
                
                print(f"User [{user['username']}] authenticated successfully")
                print(f"Login recorded @[{formatted_time}]")
                
                # Return user information
                return {
                    "user_id": user["user_id"],
                    "username": user["username"],
                    "role": user["role"], 
                    "full_name": user["full_name"],
                    "login_time": current_time,
                    "formatted_login_time": formatted_time,
                    "logout_time": user.get("logout_time"),
                    "total_session_time": user.get("total_session_time", 0)
                }
            
            return None
            
        except mysql.connector.Error as err:
            print(f"Authentication error: {err}")
            return None
            
        finally:
            # Always close cursor and commit connection
            if cursor:
                cursor.close()
            if conn:
                conn.commit()
        
    def logout(self, username):
        """
        Record logout time and update session time
        
        Args:
            username (str): Username of the user logging out
        
        Returns:
            dict: Logout information or None if failed
        """
        conn = None
        cursor = None
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get current login time
            cursor.execute(
                "SELECT login_time FROM users WHERE username = %s",
                (username,)
            )
            
            user_data = cursor.fetchone()
            if user_data and user_data.get("login_time"):
                login_time = user_data.get("login_time")
                
                # Calculate session duration
                current_time = datetime.datetime.now()
                session_duration = int((current_time - login_time).total_seconds())
                formatted_time = current_time.strftime("%I:%M %p, %m/%d/%Y")
                
                # Update logout time and session time
                cursor.execute(
                    """UPDATE users 
                       SET logout_time = CURRENT_TIMESTAMP(),
                           total_session_time = total_session_time + %s 
                       WHERE username = %s""",
                    (session_duration, username)
                )
                conn.commit()
                
                print(f"User [{username}] logged out after {session_duration} seconds")
                print(f"Logout recorded @[{formatted_time}]")
                
                return {
                    "username": username,
                    "logout_time": current_time,
                    "formatted_logout": formatted_time,
                    "session_duration": session_duration
                }
            
            return None
        
        except mysql.connector.Error as err:
            print(f"Logout error: {err}")
            return None
            
        finally:
            # Always close cursor and commit connection
            if cursor:
                cursor.close()
            if conn:
                conn.commit()