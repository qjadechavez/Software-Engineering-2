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
    def get_dialog_style():
        return """
            QDialog {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
                background: transparent;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 8px;
                selection-background-color: #007acc;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 1px solid #007acc;
                background-color: #333;
            }
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 25px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
                max-width: 120px;
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
            QFrame {
                background-color: #1e1e1e;
                border: none;
            }
        """