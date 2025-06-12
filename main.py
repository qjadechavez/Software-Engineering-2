import sys
import mysql.connector
from PyQt5 import QtWidgets
from app.ui.pages.login_page import LoginPage

def setup_database():
    """Set up the database and create necessary tables if they don't exist"""
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MySQL_",
            database="testdb",
        )
        
        print("Connected to MySQL database")

        mydb.close()
        
        return True
        
    except mysql.connector.Error as err:
        print(f"Database setup error: {err}")
        return False

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Setup database
    if not setup_database():
        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
        error_dialog.setText("Database Connection Error")
        error_dialog.setInformativeText("Could not connect to the database. Please check your database settings and try again.")
        error_dialog.setWindowTitle("Error")
        error_dialog.exec_()
        return
    
    # Create and show login window
    login_window = LoginPage()
    login_window.show()
    
    # Start the event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()