import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWebEngineWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        # Main Tab
        
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://google.com"))
        self.setCentralWidget(self.browser)
        self.showMaximized()
        
        # Navigation Bar
        navbar = QToolBar()
        self.addToolBar(navbar)
        
        back_btn = QAction("⬅️", self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)
        
        frwd_btn = QAction("➡️", self)
        frwd_btn.triggered.connect(self.browser.forward)
        navbar.addAction(frwd_btn)
        
        reload = QAction("🌀", self)
        reload.triggered.connect(self.browser.reload)
        navbar.addAction(reload)
        
        home = QAction("🏠", self)
        home.triggered.connect(self.navigate_home)
        navbar.addAction(home)
        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_url)
        navbar.addWidget(self.url_bar)
    
        self.browser.urlChanged.connect(self.update_url)
    
    
    def navigate_home(self):
        self.browser.setUrl(QUrl("https://google.com"))
        
    def navigate_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))
        
    def update_url(self, q):
        self.url_bar.setText(q.toString())
        
app = QApplication(sys.argv)
QApplication.setApplicationName("Xogy")
window = MainWindow()
app.exec_()