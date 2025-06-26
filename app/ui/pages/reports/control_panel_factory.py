from PyQt5 import QtWidgets, QtCore, QtGui
from .style_factory import StyleFactory

class ControlPanelFactory:
    """Factory class for creating search control panels"""
    
    @staticmethod
    def create_search_control(search_input, search_callback, filter_callback=None):
        """Create a consistent search and control panel
        
        Args:
            search_input: QLineEdit for search input
            search_callback: Callback for search input changes
            filter_callback: Optional callback for filter button
        
        Returns:
            QHBoxLayout containing the search controls and the filter_button reference
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
        
        # Filter button
        filter_button = QtWidgets.QPushButton("Filter")
        filter_button.setIcon(QtGui.QIcon("app/resources/images/filter.png" 
                            if QtCore.QFile("app/resources/images/filter.png").exists() 
                            else QtGui.QIcon()))
        filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
        filter_button.setFixedWidth(100)
        filter_button.setObjectName("filterButton")
        if filter_callback:
            filter_button.clicked.connect(filter_callback)
        
        # Add filter indicator (hidden by default)
        filter_indicator = QtWidgets.QLabel()
        filter_indicator.setStyleSheet("""
            QLabel {
                color: #4FC3F7;
                font-style: italic;
                padding-top: 5px;
            }
        """)
        filter_indicator.setVisible(False)
        
        # Layout for controls
        control_layout.addLayout(search_layout)
        control_layout.addWidget(search_input, 1)
        control_layout.addWidget(filter_button)
        
        # Store the filter_button and filter_indicator as attributes of the layout
        control_layout.filter_button = filter_button
        control_layout.filter_indicator = filter_indicator
        
        return control_layout
    
    @staticmethod
    def create_action_button(text, primary=True):
        """Create a standardized action button"""
        button = QtWidgets.QPushButton(text)
        button.setStyleSheet(StyleFactory.get_button_style(primary=primary))
        return button
    
    @staticmethod
    def create_export_controls():
        """Create export control buttons"""
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(10)
        
        # Export to Excel button
        excel_button = QtWidgets.QPushButton("📊 Export to Excel")
        excel_button.setStyleSheet(StyleFactory.get_button_style())
        
        # Export to PDF button
        pdf_button = QtWidgets.QPushButton("📄 Export to PDF")
        pdf_button.setStyleSheet(StyleFactory.get_button_style())
        
        layout.addWidget(excel_button)
        layout.addWidget(pdf_button)
        layout.addStretch()
        
        # Store references
        layout.excel_button = excel_button
        layout.pdf_button = pdf_button
        
        return layout