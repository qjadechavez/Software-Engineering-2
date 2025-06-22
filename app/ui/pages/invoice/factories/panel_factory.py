from PyQt5 import QtWidgets, QtCore, QtGui

class PanelFactory:
    """Factory class for creating common UI panels for invoice pages"""
    
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