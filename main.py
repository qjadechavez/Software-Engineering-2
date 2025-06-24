import sys
import mysql.connector
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QStyleFactory
from app.ui.pages.login.login_page import LoginPage
from app.utils.db_manager import DBManager

def setup_database():
    """Set up the database and check connection"""
    try:
        conn = DBManager.get_connection()
        print("Connected to MySQL database successfully")
        conn.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return False

def show_database_error():
    """Display a database connection error dialog"""
    error_dialog = QtWidgets.QMessageBox()
    error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
    error_dialog.setText("Database Connection Error")
    error_dialog.setInformativeText("Could not connect to the database. Please check your database settings and try again.")
    error_dialog.setWindowTitle("Error")
    error_dialog.exec_()

def main():
    # Initialize application
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Setup database connection
    if not setup_database():
        show_database_error()
        return
    
    # Start the application with the login window
    login_window = LoginPage()
    login_window.show()
    
    # Start the event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()