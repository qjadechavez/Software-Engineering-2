import sys
from PyQt5 import QtWidgets
from app.ui.pages.login_page import LoginPage

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show login window
    login_window = LoginPage()
    login_window.show()
    
    # Start the event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()