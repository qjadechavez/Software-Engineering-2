from PyQt5 import QtWidgets, QtCore, QtGui
from ..style_factory import StyleFactory

class BaseDialog(QtWidgets.QDialog):
    """Base dialog class for all report filter dialogs"""
    
    def __init__(self, parent=None, data=None, title="Dialog"):
        super(BaseDialog, self).__init__(parent)
        self.data = data
        self.setWindowTitle(title)
        self.setModal(True)
        self.setStyleSheet(StyleFactory.get_dialog_style())
        
    def setup_base_ui(self, width=400, height=None):
        """Set up the base UI layout"""
        self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)
        
        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # Header
        self.header_label = QtWidgets.QLabel("Filter Options")
        self.header_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding-bottom: 10px;
                border-bottom: 2px solid #007acc;
                margin-bottom: 15px;
            }
        """)
        self.main_layout.addWidget(self.header_label)
        
        # Form layout for inputs
        self.form_widget = QtWidgets.QWidget()
        self.form_layout = QtWidgets.QFormLayout(self.form_widget)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setSpacing(12)
        self.main_layout.addWidget(self.form_widget)
        
        # Spacer
        self.main_layout.addStretch()
        
        # Button layout
        self.button_widget = QtWidgets.QWidget()
        self.button_layout = QtWidgets.QHBoxLayout(self.button_widget)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.addStretch()
        
        # Cancel button
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setObjectName("cancelBtn")
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)
        
        # Save button
        self.save_button = QtWidgets.QPushButton("Apply")
        self.save_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.save_button)
        
        self.main_layout.addWidget(self.button_widget)