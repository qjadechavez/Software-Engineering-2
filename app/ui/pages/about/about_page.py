from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage

class AboutPage(BasePage):
    def __init__(self, parent=None, user_info=None):
        super(AboutPage, self).__init__(parent, title="About", user_info=user_info)
    
    def createContent(self):
        # Content area
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(15)
        
        # Create tabs for company and developers
        self.create_tabs()
        
        # Add the content area to the page layout
        self.layout.addWidget(self.content_area)
    
    def create_tabs(self):
        """Create tabs for company and developer information"""
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { 
                border: 1px solid #444; 
                background-color: #232323;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #343434;
                color: #ffffff;
                padding: 10px 20px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
                min-width: 100px;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background-color: #1a1a1a;
                border-bottom-color: #1a1a1a;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3a3a3a;
            }
        """)
        
        # Create tabs
        self.create_company_tab()
        self.create_developers_tab()
        
        self.content_layout.addWidget(self.tabs)
    
    def create_company_tab(self):
        """Create Company information tab with professional grid layout"""
        tab = QtWidgets.QWidget()
        tab.setStyleSheet("background-color: #232323;")
        main_layout = QtWidgets.QVBoxLayout(tab)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(25)
        
        # Company header
        header_widget = QtWidgets.QWidget()
        header_widget.setStyleSheet("background-color: transparent;")
        header_layout = QtWidgets.QVBoxLayout(header_widget)
        header_layout.setSpacing(8)
        
        title = QtWidgets.QLabel("Miere Beauty Lounge")
        title.setStyleSheet("""
            color: #ffffff; 
            font-size: 28px; 
            font-weight: 700; 
            margin-bottom: 5px; 
            border: none;
            letter-spacing: 1px;
            background-color: transparent;
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QtWidgets.QLabel("Premier Beauty & Wellness Establishment")
        subtitle.setStyleSheet("""
            color: #cccccc; 
            font-size: 16px; 
            font-weight: 400; 
            border: none;
            font-style: italic;
            background-color: transparent;
        """)
        subtitle.setAlignment(QtCore.Qt.AlignCenter)
        header_layout.addWidget(subtitle)
        
        main_layout.addWidget(header_widget)
        
        # Create scroll area for content
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #232323;
            }
            QScrollArea > QWidget > QWidget {
                background-color: #232323;
            }
            QScrollBar:vertical {
                background: #2a2a2a;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #555555;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #666666;
            }
        """)
        
        # Content widget for scroll area
        content_widget = QtWidgets.QWidget()
        content_widget.setStyleSheet("background-color: #232323;")
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Company overview section (keeping this as the main content)
        overview_frame = self.create_professional_section("Company Overview", [
            "Miere Beauty Lounge is a premier beauty and wellness establishment dedicated to providing exceptional skin care and beauty services. Founded with a passion for enhancing natural beauty and promoting wellness, we have become a trusted destination for clients seeking professional beauty treatments and personalized care."
        ])
        content_layout.addWidget(overview_frame)
         
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        self.tabs.addTab(tab, "Company")
    
    def create_developers_tab(self):
        """Create Developers information tab with professional grid layout"""
        tab = QtWidgets.QWidget()
        tab.setStyleSheet("background-color: #232323;")
        main_layout = QtWidgets.QVBoxLayout(tab)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(25)
        
        # Development team header
        header_widget = QtWidgets.QWidget()
        header_widget.setStyleSheet("background-color: transparent;")
        header_layout = QtWidgets.QVBoxLayout(header_widget)
        header_layout.setSpacing(8)
        
        title = QtWidgets.QLabel("Development Team")
        title.setStyleSheet("""
            color: #ffffff; 
            font-size: 28px; 
            font-weight: 700; 
            margin-bottom: 5px; 
            border: none;
            letter-spacing: 1px;
            background-color: transparent;
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QtWidgets.QLabel("Software Engineering Project Team")
        subtitle.setStyleSheet("""
            color: #cccccc; 
            font-size: 16px; 
            font-weight: 400; 
            border: none;
            font-style: italic;
            background-color: transparent;
        """)
        subtitle.setAlignment(QtCore.Qt.AlignCenter)
        header_layout.addWidget(subtitle)
        
        main_layout.addWidget(header_widget)
        
        # Create scroll area for content
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #232323;
            }
            QScrollArea > QWidget > QWidget {
                background-color: #232323;
            }
            QScrollBar:vertical {
                background: #2a2a2a;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #555555;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #666666;
            }
        """)
        
        # Content widget for scroll area
        content_widget = QtWidgets.QWidget()
        content_widget.setStyleSheet("background-color: #232323;")
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Project Information section
        project_header = QtWidgets.QLabel("Project Information")
        project_header.setStyleSheet("""
            color: #ffffff; 
            font-size: 20px; 
            font-weight: 600; 
            margin: 15px 0px 10px 0px; 
            border: none;
            background-color: transparent;
        """)
        content_layout.addWidget(project_header)
        
        # Project information grid
        project_grid = QtWidgets.QWidget()
        project_grid.setStyleSheet("background-color: transparent;")
        project_layout = QtWidgets.QGridLayout(project_grid)
        project_layout.setSpacing(20)
        
        # Project details
        project_details_frame = self.create_professional_section("Project Details", [
            "Project Name: Sales and Inventory Management System",
            "System Type: Desktop Business Application",
            "Target Business: Miere Beauty Lounge",
            "Development Period: Summer 2024-2025",
            "Deployment: Local Desktop Application"
        ])
        project_layout.addWidget(project_details_frame, 0, 0)
        
        # Academic information
        academic_frame = self.create_professional_section("Academic Information", [
            "Course: Software Engineering 2",
            "Institution: Technological Institute of the Philippines - Quezon City",
            "Department: Computer Science",
            "Academic Level: BSCS Program",
            "Semester: Summer 2024-2025",
            "Methodology: W-Model Software Development"
        ])
        project_layout.addWidget(academic_frame, 0, 1)
        
        content_layout.addWidget(project_grid)
        
        
        # System features section
        features_header = QtWidgets.QLabel("System Features")
        features_header.setStyleSheet("""
            color: #ffffff; 
            font-size: 20px; 
            font-weight: 600; 
            margin: 15px 0px 10px 0px; 
            border: none;
            background-color: transparent;
        """)
        content_layout.addWidget(features_header)
        
        # Features grid
        features_grid = QtWidgets.QWidget()
        features_grid.setStyleSheet("background-color: transparent;")
        features_layout = QtWidgets.QGridLayout(features_grid)
        features_layout.setSpacing(20)
        
        # Core business features
        core_frame = self.create_professional_section("Core Business Features", [
            "Point of Sale (POS) System: Complete transaction processing",
            "Inventory Management: Products and services tracking",
            "Customer Relationship Management: Customer data and history",
            "Business Analytics: Comprehensive reporting and insights",
            "Financial Management: Revenue tracking and financial reporting"
        ])
        features_layout.addWidget(core_frame, 0, 0)
        
        # Technical features
        technical_frame = self.create_professional_section("Technical Features", [
            "User Authentication: Secure login and session management",
            "Data Security: Encrypted data storage and transmission",
            "Backup & Recovery: Automated database backup systems",
            "Document Generation: Professional invoice and receipt printing",
            "Modern Interface: Intuitive and responsive user experience"
        ])
        features_layout.addWidget(technical_frame, 0, 1)
        
        content_layout.addWidget(features_grid)
        
        # Acknowledgments section
        acknowledgment_frame = self.create_professional_section("Acknowledgments", [
            "We extend our sincere gratitude to Ms. Melisa P. Almacen for providing comprehensive business requirements and valuable industry insights that shaped this management system.",
            "Special appreciation to our course instructor for their guidance, mentorship, and technical expertise throughout the development process.",
            "Thanks to our academic institution for providing the necessary resources, learning environment, and opportunities for practical application of software engineering principles.",
            "Recognition of the open-source community for providing robust tools and libraries that enabled the development of this comprehensive business solution.",
            "Acknowledgment of our collaborative team effort, where each member's expertise and dedication contributed to the successful completion of this project."
        ])
        content_layout.addWidget(acknowledgment_frame)
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        self.tabs.addTab(tab, "Developers")
    
    def create_professional_section(self, title, content):
        """Create a professional information section with clean typography"""
        frame = QtWidgets.QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border-radius: 8px;
                border: 1px solid #404040;
                padding: 5px;
            }
        """)
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)
        
        # Section title
        section_title = QtWidgets.QLabel(title)
        section_title.setStyleSheet("""
            color: #ffffff; 
            font-size: 16px; 
            font-weight: 600; 
            margin-bottom: 8px; 
            border: none;
            padding-bottom: 8px;
            border-bottom: 2px solid #404040;
            background-color: transparent;
        """)
        layout.addWidget(section_title)
        
        # Content
        for item in content:
            if item.strip():  # Skip empty strings
                content_label = QtWidgets.QLabel(item)
                
                # Professional styling based on content type
                if item.startswith(("Mission:", "Vision:", "Core Values:")):
                    content_label.setStyleSheet("""
                        color: #E8F5E8; 
                        font-size: 13px; 
                        margin-left: 15px; 
                        border: none; 
                        font-weight: 500;
                        line-height: 1.4;
                        background-color: transparent;
                    """)
                elif item.startswith(("Name:", "Role:", "Primary Responsibilities:")):
                    content_label.setStyleSheet("""
                        color: #E3F2FD; 
                        font-size: 13px; 
                        margin-left: 15px; 
                        border: none; 
                        font-weight: 500;
                        background-color: transparent;
                    """)
                elif item.startswith("•"):
                    content_label.setStyleSheet("""
                        color: #cccccc; 
                        font-size: 12px; 
                        margin-left: 30px; 
                        border: none;
                        line-height: 1.3;
                        background-color: transparent;
                    """)
                elif any(keyword in item for keyword in ["Project Name:", "Academic Course:", "Institution:", "Development Period:", "Technology Stack:"]):
                    content_label.setStyleSheet("""
                        color: #FFF3E0; 
                        font-size: 13px; 
                        margin-left: 15px; 
                        border: none; 
                        font-weight: 500;
                        background-color: transparent;
                    """)
                elif any(keyword in item for keyword in ["Programming Language:", "GUI Framework:", "Database:", "Design Pattern:", "Platform:"]):
                    content_label.setStyleSheet("""
                        color: #F3E5F5; 
                        font-size: 13px; 
                        margin-left: 15px; 
                        border: none; 
                        font-weight: 500;
                        background-color: transparent;
                    """)
                else:
                    # Default professional styling
                    content_label.setStyleSheet("""
                        color: #e0e0e0; 
                        font-size: 13px; 
                        margin-left: 15px; 
                        border: none;
                        line-height: 1.4;
                        background-color: transparent;
                    """)
                
                content_label.setWordWrap(True)
                layout.addWidget(content_label)
            else:
                # Add spacing for empty strings
                layout.addSpacing(8)
        
        return frame