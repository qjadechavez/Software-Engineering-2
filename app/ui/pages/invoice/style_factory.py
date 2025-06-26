class StyleFactory:
    """Factory class for creating consistent UI styles"""
    
    @staticmethod
    def get_button_style(secondary=False):
        """Get standard button style (primary or secondary)"""
        if secondary:
            return """
                QPushButton {
                    background-color: #555555;
                    color: white;
                    border-radius: 18px;
                    padding: 8px 20px;
                    font-weight: bold;
                    font-size: 13px;
                    min-height: 36px;
                    min-width: 120px;
                    max-width: 120px;
                }
                QPushButton:hover {
                    background-color: #666666;
                }
                QPushButton:pressed {
                    background-color: #444444;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #007ACC;
                    color: white;
                    border-radius: 18px;
                    padding: 8px 20px;
                    font-weight: bold;
                    font-size: 13px;
                    min-height: 36px;
                    min-width: 120px;  /* Set minimum width */
                    max-width: 120px;  /* Set maximum width */
                }
                QPushButton:hover {
                    background-color: #0099FF;
                }
                QPushButton:pressed {
                    background-color: #0066BB;
                }
            """
    
    @staticmethod
    def get_search_input_style():
        return """
            QLineEdit {
                border: 1px solid #555;
                border-radius: 18px;
                padding: 8px 15px;
                background: #2a2a2a;
                color: white;
                font-size: 13px;
                min-height: 36px;
            }
            QLineEdit:focus {
                border: 1px solid #0078d7;
                background: #323232;
            }
        """
    
    @staticmethod
    def get_services_grid_style():
        """Get style for services grid container with background"""
        return """
            QWidget {
                background-color: #1a1a1a;
                border-radius: 12px;
                border: 1px solid #333333;
                margin: 5px;
            }
        """
    
    @staticmethod
    def get_scroll_area_style():
        """Get style for scroll area"""
        return """
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #2a2a2a;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #555555;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #666666;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """
    
    @staticmethod
    def get_service_card_style():
        """Get style for service cards - clean design without borders"""
        return """
            QFrame {
                background-color: #1e1e1e;
                border-radius: 12px;
                border: none;
            }
            QFrame:hover {
                background-color: #252525;
                border: 2px solid #007ACC;
            }
            QLabel {
                border: none;
                background: transparent;
            }
        """
    
    @staticmethod
    def get_service_card_selected_style():
        """Get style for selected service cards - clean design"""
        return """
            QFrame {
                background-color: #0d4f3c;
                border-radius: 12px;
                border: 2px solid #4CAF50;
            }
            QFrame:hover {
                background-color: #0f5a44;
                border: 2px solid #66BB6A;
            }
            QLabel {
                border: none;
                background: transparent;
            }
        """
    
    @staticmethod
    def get_active_filter_button_style():
        """Get style for active filter button (blue)"""
        return """
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #42A5F5;
            }
            QPushButton:pressed {
                background-color: #1976D2;
            }
        """
    
    @staticmethod
    def get_selected_services_frame_style():
        """Get style for selected services frame"""
        return """
            QFrame {
                background-color: #1c1c1c;
                border-radius: 10px;
                border: 1px solid #444444;
                margin: 5px;
            }
        """
    
    @staticmethod
    def get_selected_services_list_style():
        """Get style for selected services list widget"""
        return """
            QListWidget {
                background-color: #2a2a2a;
                border: 1px solid #444444;
                border-radius: 4px;
                color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #444444;
                border-radius: 4px;
                margin: 2px;
                background-color: #333333;
            }
            QListWidget::item:hover {
                background-color: #3a3a3a;
            }
            QListWidget::item:selected {
                background-color: #4CAF50;
                color: white;
            }
        """
    
    @staticmethod
    def get_products_list_style():
        """Get style for products list widget"""
        return """
            QListWidget {
                background-color: #2a2a2a;
                border: 1px solid #444444;
                border-radius: 4px;
                color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 6px;
                border-radius: 3px;
                margin: 1px;
                background-color: #333333;
                font-size: 12px;
            }
            QListWidget::item:hover {
                background-color: #3a3a3a;
            }
        """
    
    @staticmethod
    def get_cancel_button_style():
        """Get style for cancel transaction button"""
        return """
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #E53935;
            }
            QPushButton:pressed {
                background-color: #C62828;
            }
        """
    
    @staticmethod
    def get_overview_container_style():
        """Get style for overview main container with background"""
        return """
            QWidget {
                background-color: #1a1a1a;
                border-radius: 12px;
                border: 1px solid #333333;
                margin: 5px;
            }
        """
    
    @staticmethod
    def get_overview_section_style():
        """Get style for overview sections"""
        return """
            QFrame {
                background-color: #1c1c1c;
                border-radius: 8px;
                border: 1px solid #444444;
                padding: 15px;
                margin: 5px;
            }
        """
    
    @staticmethod
    def get_overview_total_section_style():
        """Get style for overview total section with emphasis"""
        return """
            QFrame {
                background-color: #1c1c1c;
                border-radius: 8px;
                border: 2px solid #4CAF50;
                padding: 15px;
                margin: 5px;
            }
        """
    
    @staticmethod
    def get_overview_list_style():
        """Get style for overview list widgets"""
        return """
            QListWidget {
                background-color: #2a2a2a;
                border: 1px solid #444444;
                border-radius: 4px;
                color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 6px;
                border-radius: 3px;
                margin: 1px;
                color: white;
                background-color: transparent;
                border: none;
                font-size: 12px;
            }
            QListWidget::item:hover {
                background-color: #3a3a3a;
            }
        """
    
    @staticmethod
    def get_dialog_style():
        """Get style for dialogs"""
        return """
            QDialog {
                background-color: rgba(0, 0, 0, 0.8);
            }
            QLabel {
                color: white;
                background: transparent;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QTextEdit {
                padding: 8px;
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #444444;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus, QTextEdit:focus {
                border: 1px solid #2196F3;
            }
            QPushButton {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton#cancelBtn {
                background-color: #666666;
            }
            QPushButton#cancelBtn:hover {
                background-color: #777777;
            }
            QPushButton#cancelBtn:pressed {
                background-color: #555555;
            }
        """
    
    @staticmethod
    def get_main_container_style():
        return """
            QFrame {
                background-color: #1E1E1E;
                border-radius: 16px;
                padding: 12px;
            }
        """

    @staticmethod
    def get_section_frame_style():
        return """
            QFrame {
                background-color: #2A2A2A;
                border-radius: 8px;
                padding: 8px;
            }
        """

    @staticmethod
    def get_separator_style():
        # a slightly lighter line for separation
        return "color: #3C3C3C;"

    @staticmethod
    def get_standard_font():
        # returns a QFont string for consistent typography
        return "font-family: 'Segoe UI';"

