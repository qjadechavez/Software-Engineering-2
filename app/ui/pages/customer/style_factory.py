class StyleFactory:
    """Factory class for consistent styling across components"""
    
    @staticmethod
    def get_tab_style():
        return """
            QTabWidget::pane { 
                border: 1px solid #444; 
                background-color: #232323;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #343434;
                color: #ffffff;
                padding: 10px 30px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
                min-width: 120px;
                font-size: 13px;
            }
            QTabBar::tab:selected {
                background-color: #1a1a1a;
                border-bottom-color: #1a1a1a;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3a3a3a;
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
    def get_button_style(secondary=False):
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
    def get_active_filter_button_style():
        return """
            QPushButton {
                background-color: #007ACC;  /* Same blue as primary buttons */
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
                background-color: #0099FF;
            }
            QPushButton:pressed {
                background-color: #0066BB;
            }
        """
    
    @staticmethod
    def get_table_style():
        return """
            QTableWidget {
                background-color: #1e1e1e;
                gridline-color: #444;
                color: white;
                border-radius: 5px;
                border: 1px solid #555;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #2c2c2c;
                color: white;
                padding: 8px;
                border: 1px solid #444;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
                background-color: #1e1e1e;
            }
            QTableWidget::item:selected {
                background-color: #0078d7;
            }
            QScrollBar:vertical {
                background: #2a2a2a;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #666;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar:horizontal {
                background: #2a2a2a;
                height: 12px;
            }
            QScrollBar::handle:horizontal {
                background: #666;
                border-radius: 5px;
                min-width: 20px;
            }
        """
    
    @staticmethod
    def get_dialog_style():
        return """
            QDialog {
                background-color: #1e1e1e;  /* Dark background for the entire dialog */
            }
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
                background: transparent;
            }
            QLineEdit, QTextEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 8px;
                selection-background-color: #007acc;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 1px solid #007acc;
                background-color: #333;
            }
            QCheckBox {
                color: white;
                font-size: 14px;
                background: transparent;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                background: #2d2d2d;
                border: 1px solid #444;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background: #007acc;
                border: none;
                image: url(app/resources/images/check.png);
            }
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 25px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;  /* Set minimum width */
                max-width: 120px;  /* Set maximum width */
            }
            QPushButton:hover {
                background-color: #0088e0;
            }
            QPushButton:pressed {
                background-color: #006bb3;
            }
            QPushButton#cancelBtn {
                background-color: #555;
            }
            QPushButton#cancelBtn:hover {
                background-color: #666;
            }
            QPushButton#cancelBtn:pressed {
                background-color: #444;
            }
            /* Style for the dialog frame */
            QFrame {
                background-color: #1e1e1e;
                border: none;
            }
        """
    
    @staticmethod
    def get_receipt_style():
        return """
            QWidget#receiptContent {
                background-color: white;
                border: 1px solid #555;
                border-radius: 5px;
            }
            QLabel {
                color: #333333;
                background-color: transparent;
            }
            QLabel#receiptTitle {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
            }
            QLabel#receiptHeading {
                font-size: 12px;
                font-weight: bold;
                color: #333333;
            }
            QLabel#receiptLabel {
                font-size: 10px;
                font-weight: bold;
                color: #333333;
            }
            QLabel#receiptValue {
                font-size: 10px;
                color: #333333;
            }
            QLabel#totalValue {
                font-size: 12px;
                font-weight: bold;
                color: #333333;
            }
            QTableWidget {
                background-color: white;
                color: #333333;
                border: none;
                font-size: 10px;
            }
            QTableWidget::item {
                padding: 2px;
            }
        """