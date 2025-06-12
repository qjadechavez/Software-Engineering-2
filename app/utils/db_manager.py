import mysql.connector

class DBManager:
    """Manager for handling database connections"""
    
    # Database configuration
    DB_CONFIG = {
        "host": "localhost",
        "user": "root",
        "password": "MySQL_",
        "database": "testdb",
    }
    
    @staticmethod
    def get_connection():
        """
        Get a new database connection
        
        Returns:
            connection: MySQL connection object
        """
        try:
            conn = mysql.connector.connect(**DBManager.DB_CONFIG)
            return conn
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
            raise