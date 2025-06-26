from PyQt5 import QtWidgets, QtCore, QtGui
from .style_factory import StyleFactory

class ControlPanelFactory:
    """Factory class for creating search control panels"""
    
    @staticmethod
    def create_search_control(search_input, add_button_text, add_button_callback, search_callback, filter_callback=None):
        """Create a consistent search and control panel"""
        control_layout = QtWidgets.QHBoxLayout()
        control_layout.setSpacing(10)
        
        # Configure search input
        search_input.setPlaceholderText("Search...")
        search_input.setStyleSheet(StyleFactory.get_search_input_style())
        search_input.textChanged.connect(search_callback)
        
        # Search icon and label
        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setSpacing(5)
        
        search_label = QtWidgets.QLabel("Search:")
        search_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; border: none;")
        
        search_layout.addWidget(search_label)
        
        # Add button
        add_button = QtWidgets.QPushButton(add_button_text)
        add_button.setStyleSheet(StyleFactory.get_button_style())
        add_button.clicked.connect(add_button_callback)
        
        # Layout for controls
        control_layout.addLayout(search_layout)
        control_layout.addWidget(search_input, 1)
        control_layout.addWidget(add_button)
        
        return control_layout