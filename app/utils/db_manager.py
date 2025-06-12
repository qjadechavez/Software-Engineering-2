import mysql.connector
from mysql.connector import Error
import os
import json
from pathlib import Path

class DBManager:
    """Manager for handling database connections with improved error handling"""
    
    # Default database configuration
    DEFAULT_CONFIG = {
        "host": "localhost",
        "user": "root",
        "password": "MySQL_",
        "database": "testdb",
    }
    
    # Singleton connection instance
    _connection = None
    
    @classmethod
    def get_config(cls):
        """
        Get database configuration from config file or use defaults
        
        Returns:
            dict: Database configuration
        """
        try:
            # Try to load config from a file (for easier configuration changes)
            config_path = Path(__file__).parent.parent.parent / "config" / "database.json"
            
            if config_path.exists():
                with open(config_path, "r") as config_file:
                    return json.load(config_file)
            
        except Exception as e:
            print(f"Warning: Could not load database config from file: {e}")
            print("Using default database configuration")
        
        # Return default configuration
        return cls.DEFAULT_CONFIG
    
    @classmethod
    def get_connection(cls):
        """
        Get a database connection (creates a new one or reuses existing if valid)
        
        Returns:
            connection: MySQL connection object
        
        Raises:
            mysql.connector.Error: If connection fails
        """
        try:
            # Check if we have a valid connection
            if cls._connection and cls._connection.is_connected():
                return cls._connection
            
            # Create a new connection
            config = cls.get_config()
            cls._connection = mysql.connector.connect(**config)
            return cls._connection
            
        except Error as err:
            print(f"Database connection error: {err}")
            raise
    
    @classmethod
    def close_connection(cls):
        """Close the database connection if it exists"""
        if cls._connection and cls._connection.is_connected():
            cls._connection.close()
            cls._connection = None
            print("Database connection closed")