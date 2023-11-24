import sys, ctypes, os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtNetwork import QNetworkCookie
from urllib.parse import unquote, urlsplit

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        # Create a QWebEngineProfile to manage settings, including cookies
        self.profile = QWebEngineProfile.defaultProfile()
        self.cookie_store = self.profile.cookieStore()
        self.cookie_store.cookieAdded.connect(self.cookie_added)

        # Main Tab
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Initial tab
        self.add_new_tab(QUrl("https://google.com"))

        # Navigation Bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction(QIcon('back.png'), "Back", self)
        back_btn.triggered.connect(self.current_tab().back)
        navbar.addAction(back_btn)

        frwd_btn = QAction(QIcon('forward.png'), "Forward", self)
        frwd_btn.triggered.connect(self.current_tab().forward)
        navbar.addAction(frwd_btn)

        reload = QAction(QIcon('reload.png'), "Reload", self)
        reload.triggered.connect(self.current_tab().reload)
        navbar.addAction(reload)

        home = QAction(QIcon('home.png'), "Home", self)
        home.triggered.connect(self.navigate_home)
        navbar.addAction(home)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_url)
        navbar.addWidget(self.url_bar)

        search_icon = QLabel()
        search_icon.setPixmap(QPixmap('search.png'))
        navbar.addWidget(search_icon)

        # "+" button to add a new tab
        new_tab_btn = QAction(QIcon('new_tab.png'), "New Tab", self)
        new_tab_btn.triggered.connect(self.add_new_tab)
        navbar.addAction(new_tab_btn)


        self.tabs.currentChanged.connect(self.tab_changed)
        self.cookie_store.cookieAdded.connect(self.cookie_added)
        self.current_tab().urlChanged.connect(lambda q, browser=self.current_tab(): self.update_url(q, browser))

        # Status Bar
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        remove_tab_btn = QAction(QIcon('remove_tab.png'), "Remove Tab", self)
        remove_tab_btn.triggered.connect(self.remove_current_tab)
        navbar.addAction(remove_tab_btn)

        self.current_tab().page().profile().downloadRequested.connect(self.download_requested)


    def download_requested(self, download_item):
        # Get the suggested file name and decode any URL-encoded characters
        suggested_file_name = unquote(download_item.suggestedFileName())

        # Extract the original file name and extension from the download item's URL
        url_path = urlsplit(download_item.url().toString()).path
        original_file_name = os.path.basename(url_path)
        _, original_file_extension = os.path.splitext(original_file_name)

        # If the suggested file name doesn't already have an extension, append the original extension
        if not os.path.splitext(suggested_file_name)[1]:
            suggested_file_name += original_file_extension

        # Ask the user for the download location
        default_location = os.path.expanduser("~/Downloads")  # Default Downloads directory
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", os.path.join(default_location, suggested_file_name), f"All Files (*);;{suggested_file_name}")

        if file_path:
            # Set the download item's path and start the download
            download_item.setPath(file_path)
            download_item.accept()
    
    
    def add_new_tab(self, url=None):
        if url is None or not isinstance(url, str):
            url = "https://google.com"

        try:
            url = QUrl(url)
        except ValueError:
            url = QUrl("https://google.com")

        browser = QWebEngineView()
        browser.setUrl(url)
        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(index)
        browser.urlChanged.connect(lambda q, browser=browser: self.update_url(q, browser))


    def current_tab(self):
        return self.tabs.currentWidget()

    def navigate_home(self):
        self.current_tab().setUrl(QUrl("https://google.com"))

    def navigate_url(self):
        input_text = self.url_bar.text()

        # Check if the input looks like a URL
        if "." in input_text and " " not in input_text:
            url = QUrl.fromUserInput(input_text)
        else:
            # If not, perform a search using a search engine (Google in this case)
            url = QUrl("https://www.google.com/search?q=" + input_text)

        self.current_tab().setUrl(url)

    def update_url(self, q, browser):
        if browser == self.current_tab():
            self.url_bar.setText(q.toString())

    def tab_changed(self, index):
        current_browser = self.tabs.widget(index)
        if current_browser is not None:
            current_browser.urlChanged.connect(lambda q, browser=current_browser: self.update_url(q, browser))


    def cookie_added(self, cookie):
        print(f"Cookie added: {cookie.name()}={cookie.value()}")
        
        
    def remove_current_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index != -1:
            widget = self.tabs.widget(current_index)
            widget.close()  # Close the widget (removing the tab)
            self.tabs.removeTab(current_index)


def hide_console():
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    
    SW_HIDE = 0
    hwnd = kernel32.GetConsoleWindow()
    user32.ShowWindow(hwnd, SW_HIDE)

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

    # Start the window maximized
    window.showMaximized()

    # Hide the console window
    hide_console()

    sys.exit(app.exec_())
