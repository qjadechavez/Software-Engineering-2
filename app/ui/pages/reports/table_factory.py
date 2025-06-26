from PyQt5 import QtWidgets, QtCore, QtGui
from .style_factory import StyleFactory

class TableFactory:
    """Factory for creating standardized tables across the reports page"""
    
    @staticmethod
    def create_table():
        """Create a standardized table widget"""
        table = QtWidgets.QTableWidget()
        
        # Basic table properties
        table.setStyleSheet(StyleFactory.get_table_style())
        table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        table.setAlternatingRowColors(False)
        table.verticalHeader().setVisible(False)
        table.setSortingEnabled(True)
        table.setShowGrid(True)
        
        # Make columns and rows not resizable
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        table.horizontalHeader().setStretchLastSection(False)
        
        return table
    
    @staticmethod
    def configure_table_columns(table, columns, screen_width):
        """Configure table columns with relative widths"""
        table.setColumnCount(len(columns))
        
        # Set headers
        headers = [col[0] for col in columns]
        table.setHorizontalHeaderLabels(headers)
        
        # Calculate and set column widths
        available_width = int(screen_width * 0.75)  # Use 75% of screen width
        
        for i, (header, ratio) in enumerate(columns):
            width = int(available_width * ratio)
            table.setColumnWidth(i, width)
        
        # Enable stretching for the last column
        header = table.horizontalHeader()
        header.setStretchLastSection(True)