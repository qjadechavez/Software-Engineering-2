from PyQt5 import QtWidgets, QtCore, QtGui
from ..style_factory import StyleFactory

class BaseDialog(QtWidgets.QDialog):
    """Base dialog class with common functionality for both dialogs"""
    
    def __init__(self, parent=None, item=None, title=""):
        super(BaseDialog, self).__init__(parent)
        self.item = item
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # Common attributes that will be set by child classes
        self.header_label = None
        self.name_input = None
        self.category_input = None
        self.description_input = None
        self.price_input = None
        self.availability_checkbox = None
        
        # Define old_pos for drag support
        self.old_pos = None
    
    def setup_base_ui(self, dialog_height):
        """Set up the base dialog UI with common elements
        
        Args:
            dialog_height: Height of the dialog
        """
        # Set dialog size
        self.resize(550, dialog_height)
        
        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create main container with rounded corners
        self.container = QtWidgets.QFrame(self)
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
            #container {
                background-color: rgba(35, 35, 35, 0.95);
                border-radius: 12px;
                border: 1px solid rgba(100, 100, 100, 0.3);
            }
        """)
        
        # Container layout
        container_layout = QtWidgets.QVBoxLayout(self.container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)
        
        # Header with close button
        header_layout = QtWidgets.QHBoxLayout()
        
        self.header_label = QtWidgets.QLabel("Dialog Header")
        self.header_label.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
        """)
        
        close_button = QtWidgets.QPushButton("×")
        close_button.setObjectName("closeBtn")  # Add unique object name
        close_button.setFixedSize(35, 35)
        close_button.setStyleSheet("""
            QPushButton#closeBtn {
                background-color: transparent;
                color: #aaa;
                font-size: 20px;
                font-weight: bold;
                border: none;
                border-radius: 17px;
                margin: 0px 0px 0px 0px;
                line-height: 33px;
                min-width: 35px;  /* Override global min-width */
                max-width: 35px;  /* Override global max-width */
            }
            QPushButton#closeBtn:hover {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border-radius: 17px;
            }
            QPushButton#closeBtn:pressed {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 17px;
            }
        """)
        close_button.clicked.connect(self.reject)
        
        header_layout.addWidget(self.header_label)
        header_layout.addStretch()
        header_layout.addWidget(close_button)
        
        container_layout.addLayout(header_layout)
        
        # Add separator
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        separator.setStyleSheet("background-color: rgba(100, 100, 100, 0.3); margin: 0px 0px 10px 0px;")
        container_layout.addWidget(separator)
        
        # Create a scroll area for the form
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #292929;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #555;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Form content will be added by child classes
        self.form_widget = QtWidgets.QWidget()
        self.form_widget.setStyleSheet("background: transparent;")
        self.form_layout = QtWidgets.QFormLayout(self.form_widget)
        self.form_layout.setContentsMargins(5, 5, 5, 5)
        self.form_layout.setSpacing(15)
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.form_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        
        # Apply global styles
        self.setStyleSheet(StyleFactory.get_dialog_style())
        
        self.scroll_area.setWidget(self.form_widget)
        container_layout.addWidget(self.scroll_area, 1)
        
        # Add bottom separator
        bottom_separator = QtWidgets.QFrame()
        bottom_separator.setFrameShape(QtWidgets.QFrame.HLine)
        bottom_separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        bottom_separator.setStyleSheet("background-color: rgba(100, 100, 100, 0.3); margin: 10px 0px 10px 0px;")
        container_layout.addWidget(bottom_separator)
        
        # Button area
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(10)
        
        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.setObjectName("cancelBtn")
        cancel_button.clicked.connect(self.reject)
        
        self.save_button = QtWidgets.QPushButton("Save")
        
        # Add spacer to push buttons to the right
        button_layout.addStretch(1)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(self.save_button)
        
        container_layout.addLayout(button_layout)
        
        # Add container to main layout
        main_layout.addWidget(self.container)
        
        # Enable dragging the dialog
        self.container.mousePressEvent = self.mousePressEvent
        self.container.mouseMoveEvent = self.mouseMoveEvent
        self.container.mouseReleaseEvent = self.mouseReleaseEvent

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()
    
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = None