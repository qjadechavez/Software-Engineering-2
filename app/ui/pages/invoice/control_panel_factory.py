from PyQt5 import QtWidgets, QtCore, QtGui
from .style_factory import StyleFactory

class ControlPanelFactory:
    """Factory class for creating common UI panels for invoice pages"""
    
    
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
        search_input.setPlaceholderText("Search services...")
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
    
    @staticmethod
    def create_service_card(service_data, on_select_callback=None):
        """Create a service card panel"""
        card = QtWidgets.QFrame()
        card.setFrameShape(QtWidgets.QFrame.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border-radius: 8px;
                border: 1px solid #444444;
            }
            QFrame:hover {
                background-color: #323232;
                border: 1px solid #666666;
            }
        """)
        card.setCursor(QtCore.Qt.PointingHandCursor)
        
        # Card layout
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)
        
        # Service name
        name_label = QtWidgets.QLabel(service_data['service_name'])
        name_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        layout.addWidget(name_label)
        
        # Category
        category_label = QtWidgets.QLabel(f"Category: {service_data['category']}")
        category_label.setStyleSheet("color: #cccccc; font-size: 12px;")
        layout.addWidget(category_label)
        
        # Price
        price_label = QtWidgets.QLabel(f"Price: ₱{float(service_data['price']):.2f}")
        price_label.setStyleSheet("color: #4CAF50; font-weight: bold; font-size: 14px;")
        layout.addWidget(price_label)
        
        # Description (if available)
        if service_data.get('description'):
            desc_text = service_data['description']
            # Truncate long descriptions
            if len(desc_text) > 50:
                desc_text = desc_text[:47] + "..."
            
            desc_label = QtWidgets.QLabel(desc_text)
            desc_label.setStyleSheet("color: #cccccc; font-size: 12px; font-style: italic;")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        # Store service ID as a property of the card for reference
        card.service_id = service_data['service_id']
        
        # Connect click event
        if on_select_callback:
            card.mousePressEvent = lambda event: on_select_callback(service_data)
        
        return card
    
    @staticmethod
    def create_form_group(label_text, input_widget):
        """Create a labeled form group"""
        group = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(group)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(5)
        
        label = QtWidgets.QLabel(label_text)
        label.setStyleSheet("color: #cccccc; font-size: 12px;")
        
        layout.addWidget(label)
        layout.addWidget(input_widget)
        
        return group
    
    @staticmethod
    def create_section(title):
        """Create a section with title"""
        section = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(section)
        layout.setContentsMargins(0, 0, 0, 15)
        layout.setSpacing(10)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        
        layout.addWidget(title_label)
        
        return section, layout
    
    @staticmethod
    def create_action_button(text, primary=True):
        """Create a styled action button"""
        button = QtWidgets.QPushButton(text)
        
        if primary:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0d8bf2;
                }
                QPushButton:pressed {
                    background-color: #0c7ed9;
                }
            """)
        else:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #555555;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #666666;
                }
                QPushButton:pressed {
                    background-color: #4a4a4a;
                }
            """)
        
        return button