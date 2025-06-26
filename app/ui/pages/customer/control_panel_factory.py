from PyQt5 import QtWidgets, QtCore, QtGui
from .style_factory import StyleFactory

class ControlPanelFactory:
    """Factory class for creating consistent control panels"""
    
    @staticmethod
    def create_search_control(search_input, search_callback, filter_callback=None):
        """Create a search control panel without add button
        
        Args:
            search_input: The QLineEdit widget for search
            search_callback: Function to call when search text changes
            filter_callback: Optional callback for filter button
            
        Returns:
            QHBoxLayout: The control panel layout with filter_button attribute if filter_callback is provided
        """
        control_layout = QtWidgets.QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 10)
        
        # Search icon
        search_icon = QtWidgets.QLabel()
        search_icon.setPixmap(QtGui.QPixmap("app/resources/images/search.png").scaled(16, 16, 
                            QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation) 
                        if QtCore.QFile("app/resources/images/search.png").exists() 
                        else QtGui.QPixmap())
        search_icon.setStyleSheet("margin-right: 5px;")
        
        # Search container (for styling with icon)
        search_container = QtWidgets.QHBoxLayout()
        search_container.setSpacing(0)
        search_container.addWidget(search_icon)
        
        # Configure search input
        search_input.setMinimumHeight(36)
        search_input.setStyleSheet(StyleFactory.get_search_input_style())
        search_input.setPlaceholderText("Search customers...")
        search_input.textChanged.connect(search_callback)
        
        # Add to search container
        search_container.addWidget(search_input)
        
        # Filter button (optional)
        if filter_callback:
            filter_button = QtWidgets.QPushButton("Filter")
            filter_button.setCursor(QtCore.Qt.PointingHandCursor)
            filter_button.setMinimumHeight(36)
            filter_button.setFixedWidth(120)
            filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
            filter_button.clicked.connect(filter_callback)
            
            # Add filter indicator (hidden by default)
            filter_indicator = QtWidgets.QLabel("•")
            filter_indicator.setStyleSheet("""
                color: #4CAF50;
                font-size: 24px;
                font-weight: bold;
                margin-right: -10px;
            """)
            filter_indicator.setVisible(False)
            
            # Store references as attributes
            control_layout.filter_button = filter_button
            control_layout.filter_indicator = filter_indicator
        
        # Search label
        search_label = QtWidgets.QLabel("Search:")
        search_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        
        # Layout for search controls
        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setSpacing(5)
        search_layout.addWidget(search_icon)
        search_layout.addWidget(search_label)
        
        # Add widgets to layout
        control_layout.addLayout(search_layout)
        control_layout.addLayout(search_container, 1)
        
        # Add filter button and indicator if provided
        if filter_callback:
            control_layout.addWidget(filter_indicator)
            control_layout.addWidget(filter_button)
        
        return control_layout