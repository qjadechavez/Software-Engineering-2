from PyQt5 import QtWidgets, QtCore, QtGui
from .style_factory import StyleFactory

class ControlPanelFactory:
    """Factory class for creating search control panels"""
    
    @staticmethod
    def create_search_control(search_input, add_button_text, add_button_callback, search_callback):
        """Create a consistent search and control panel
        
        Args:
            search_input: QLineEdit for search input
            add_button_text: Text for the add button
            add_button_callback: Callback for the add button
            search_callback: Callback for search input changes
        
        Returns:
            QHBoxLayout containing the search controls
        """
        control_layout = QtWidgets.QHBoxLayout()
        control_layout.setSpacing(10)
        
        # Configure search input
        search_input.setPlaceholderText("Search...")
        search_input.setStyleSheet(StyleFactory.get_search_input_style())
        search_input.textChanged.connect(search_callback)
        
        # Search icon and label
        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setSpacing(5)
        
        search_icon = QtWidgets.QLabel()
        search_icon.setPixmap(QtGui.QPixmap("app/resources/images/search.png").scaledToHeight(16) 
                            if QtCore.QFile("app/resources/images/search.png").exists() 
                            else QtGui.QPixmap())
        search_icon.setStyleSheet("color: white; margin-right: 5px;")
        
        search_label = QtWidgets.QLabel("Search:")
        search_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        
        search_layout.addWidget(search_icon)
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