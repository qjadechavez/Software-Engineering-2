class StyleFactory:
    """Factory class for consistent styling across login components"""
    
    @staticmethod
    def get_input_field_style():
        """Style for input fields"""
        return (
            "border: 1px solid #CCCCCC; "
            "border-radius: 5px; "
            "padding: 10px;"
        )
    
    @staticmethod
    def get_label_style():
        """Style for form labels"""
        return "color: #555555;"
    
    @staticmethod
    def get_button_style(is_primary=True):
        """Style for buttons"""
        if is_primary:
            return (
                "background-color: #232323; "
                "color: white; "
                "border-radius: 5px; "
                "border: none;"
            )
        else:
            return (
                "QPushButton {"
                "    background-color: rgba(226, 241, 99, 0.15); "
                "    color: #E2F163; "
                "    border: 1px solid #E2F163; "
                "    border-radius: 22px; "
                "    padding: 8px 15px;"
                "    text-align: left;"
                "}"
                "QPushButton:hover {"
                "    background-color: rgba(226, 241, 99, 0.25); "
                "}"
                "QPushButton:pressed {"
                "    background-color: rgba(226, 241, 99, 0.35); "
                "}"
            )
    
    @staticmethod
    def get_error_style():
        """Style for error messages"""
        return "color: #FF3333;"