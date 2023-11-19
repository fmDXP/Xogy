import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtNetwork import QNetworkCookie

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        settings = QWebEngineSettings.globalSettings()
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        
        
        # Create a QWebEngineProfile to manage settings, including cookies
        self.profile = QWebEngineProfile.defaultProfile()
        self.cookie_store = self.profile.cookieStore()
        self.cookie_store.cookieAdded.connect(self.cookie_added)

        # Main Tab
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://google.com"))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # Navigation Bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction(QIcon('back.png'), "Back", self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        frwd_btn = QAction(QIcon('forward.png'), "Forward", self)
        frwd_btn.triggered.connect(self.browser.forward)
        navbar.addAction(frwd_btn)

        reload = QAction(QIcon('reload.png'), "Reload", self)
        reload.triggered.connect(self.browser.reload)
        navbar.addAction(reload)

        home = QAction(QIcon('home.png'), "Home", self)
        home.triggered.connect(self.navigate_home)
        navbar.addAction(home)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

        # Status Bar
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://google.com"))

    def navigate_url(self):
        input_text = self.url_bar.text()

        # Check if the input looks like a URL
        if "." in input_text and " " not in input_text:
            url = QUrl.fromUserInput(input_text)
        else:
            # If not, perform a search using a search engine (Google in this case)
            url = QUrl("https://www.google.com/search?q=" + input_text)

        self.browser.setUrl(url)

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def cookie_added(self, cookie):
        print(f"Cookie added: {cookie.name()}={cookie.value()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Xogy")

    # Set the application style to Fusion for a more modern look
    app.setStyle("Fusion")

    window = MainWindow()
    window.setWindowTitle("Xogy Browser")

    # Apply a style sheet for a better look
    style_sheet = """
        QMainWindow {
            background-color: #f0f0f0;
        }
        QToolBar {
            border: 1px solid #c4c4c4;
            background-color: #f0f0f0;
        }
        QLineEdit {
            padding: 5px;
            border: 1px solid #c4c4c4;
            border-radius: 5px;
        }
    """
    window.setStyleSheet(style_sheet)

    # Set window icon
    app_icon = QIcon('icon.png')
    window.setWindowIcon(app_icon)

    # Set icons for buttons
    app.setWindowIcon(app_icon)
    sys.exit(app.exec_())
