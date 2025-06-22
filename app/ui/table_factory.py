import tkinter as tk
from tkinter import ttk

class TableFactory:
    """Factory for creating consistent tables across the application"""
    
    @staticmethod
    def create_table(parent, columns, column_widths=None, height=10):
        """Create a styled table (Treeview) with consistent look
        
        Args:
            parent: Parent widget
            columns (list): List of column names
            column_widths (dict, optional): Dictionary mapping column names to widths
            height (int): Number of rows to display
            
        Returns:
            ttk.Treeview widget
        """
        # Style for the table
        style = ttk.Style()
        style.configure("App.Treeview", 
                        background="white",
                        fieldbackground="white",
                        rowheight=35)
        style.configure("App.Treeview.Heading", 
                        font=("Segoe UI", 10, "bold"),
                        foreground="#333333")
        style.map("App.Treeview", 
                  background=[("selected", "#e7f3fd")],
                  foreground=[("selected", "#333333")])
        
        # Create table with configured style
        table = ttk.Treeview(
            parent, 
            columns=columns,
            show="headings",
            style="App.Treeview",
            height=height
        )
        
        # Set up columns
        for i, col in enumerate(columns):
            # Calculate column width if not specified
            width = 100  # Default width
            if column_widths and col in column_widths:
                width = column_widths[col]
                
            table.column(col, width=width, minwidth=50)
            table.heading(col, text=col)
            
        return table
    
    @staticmethod
    def add_scrollbars(parent, table):
        """Add scrollbars to a table
        
        Args:
            parent: Parent widget
            table: The table widget (ttk.Treeview)
            
        Returns:
            Tuple of (table, y_scrollbar, x_scrollbar)
        """
        # Create vertical scrollbar
        y_scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=table.yview)
        table.configure(yscrollcommand=y_scrollbar.set)
        
        # Create horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=table.xview)
        table.configure(xscrollcommand=x_scrollbar.set)
        
        # Arrange table and scrollbars
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        return table, y_scrollbar, x_scrollbar
    
    @staticmethod
    def populate_sample_data(table, columns, data):
        """Populate table with sample data
        
        Args:
            table: The table widget (ttk.Treeview)
            columns (list): List of column names
            data (list): List of data rows (each row should have same number of items as columns)
        """
        # Clear existing items
        for item in table.get_children():
            table.delete(item)
            
        # Insert data
        for row in data:
            table.insert("", tk.END, values=row)
            
        return table
