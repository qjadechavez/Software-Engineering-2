from PyQt5 import QtWidgets
from .style_factory import StyleFactory

class TableFactory:
    """Factory class for creating consistent tables"""
    
    @staticmethod
    def create_table():
        """Create a base table with common configuration"""
        table = QtWidgets.QTableWidget()
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
    def configure_table_columns(table, column_data, screen_width):
        """Configure table columns with headers and widths
        
        Args:
            table: QTableWidget to configure
            column_data: List of tuples (header, width_percentage)
            screen_width: Total screen width to calculate from
        """
        # Calculate available width
        table_width = screen_width - 300
        
        # Set column count
        table.setColumnCount(len(column_data))
        
        # Set headers and column widths
        headers = [col[0] for col in column_data]
        table.setHorizontalHeaderLabels(headers)
        
        # Make the table stretch to fill available space
        table.horizontalHeader().setStretchLastSection(True)
        
        for idx, (_, width_pct) in enumerate(column_data[:-1]):
            table.setColumnWidth(idx, int(table_width * width_pct))