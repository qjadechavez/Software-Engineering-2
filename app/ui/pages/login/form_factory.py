from PyQt5 import QtWidgets, QtGui, QtCore
from .style_factory import StyleFactory

class FormFactory:
    """Factory for creating form elements with consistent styling"""
    
    @staticmethod
    def create_input_field(parent, placeholder="", password_mode=False):
        """Create a consistently styled input field"""
        field = QtWidgets.QLineEdit(parent)
        field.setFont(QtGui.QFont("Segoe UI", 12))
        field.setStyleSheet(StyleFactory.get_input_field_style())
        field.setPlaceholderText(placeholder)
        
        if password_mode:
            field.setEchoMode(QtWidgets.QLineEdit.Password)
            
        return field
    
    @staticmethod
    def create_label(parent, text, font_size=10, bold=False):
        """Create a consistently styled label"""
        label = QtWidgets.QLabel(parent)
        font = QtGui.QFont("Segoe UI", font_size)
        if bold:
            font.setBold(True)
        label.setFont(font)
        label.setText(text)
        label.setStyleSheet(StyleFactory.get_label_style())
        return label
    
    @staticmethod
    def create_button(parent, text, primary=True, icon_path=None):
        """Create a consistently styled button"""
        button = QtWidgets.QPushButton(parent)
        button.setFont(QtGui.QFont("Segoe UI", 12, QtGui.QFont.Bold if primary else QtGui.QFont.Normal))
        button.setText(text)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(StyleFactory.get_button_style(primary))
        
        if icon_path:
            button.setIcon(QtGui.QIcon(icon_path))
            button.setIconSize(QtCore.QSize(20, 20))
        
        return button
        
    @staticmethod
    def create_link_label(parent, text, align_center=True):
        """Create a link label with consistent styling"""
        link = QtWidgets.QLabel(parent)
        link.setFont(QtGui.QFont("Segoe UI", 10))
        link.setText(text)
        if align_center:
            link.setAlignment(QtCore.Qt.AlignCenter)
        link.setOpenExternalLinks(False)
        return link