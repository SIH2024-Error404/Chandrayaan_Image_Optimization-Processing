import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt
from gui import MainWindow  # Import the main GUI

class LandingPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERROR404 - Lunar Image Processing - Welcome")
        self.setGeometry(100, 100, 600, 400)

        # Central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout
        layout = QVBoxLayout(self.central_widget)

        # Project details
        intro_text = ("<h2>ERROR404 - Lunar Image Processing Project</h2>"
                      "<p>Welcome to the Lunar Image Processing Application. This tool helps in the "
                      "pre-processing, enhancement, denoising, and analysis of lunar images, particularly "
                      "those from Permanently Shadowed Regions (PSR) in lunar craters.</p>"
                      "<h3>Steps involved:</h3>"
                      "<ul>"
                      "<li>Loading Images</li>"
                      "<li>Pre-processing: Noise Reduction, Contrast Adjustment</li>"
                      "<li>Image Enhancement: Histogram Equalization, Retinex</li>"
                      "<li>Denoising: Wavelet Transform, Deep Learning-Based Denoising</li>"
                      "<li>PSR Detection and Analysis</li>"
                      "<li>Saving: Processed images will be saved in the 'processed' directory under 'data'</li>"
                      "</ul>"
                      "<p>Note: The images used in this application are taken from the image capturing "
                      "done by Chandrayaan 2. You can browse these images at the following link: "
                      "<a href='https://pradan.issdc.gov.in/ch2/protected/browse.xhtml?id=ohrc'>Chandrayaan 2 OHRC Images</a></p>"
                      "<p>Click 'Continue' to proceed to the main application or 'Exit' to close.</p>")
        self.intro_label = QLabel(intro_text, self)
        self.intro_label.setAlignment(Qt.AlignCenter)
        self.intro_label.setWordWrap(True)
        layout.addWidget(self.intro_label)

        # Continue button
        self.continueButton = QPushButton('Continue', self)
        self.continueButton.clicked.connect(self.open_main_gui)
        layout.addWidget(self.continueButton)

        # Exit button
        self.exitButton = QPushButton('Exit', self)
        self.exitButton.clicked.connect(self.close_application)
        layout.addWidget(self.exitButton)

    def open_main_gui(self):
        self.main_window = MainWindow()  # Create an instance of MainWindow from gui.py
        self.main_window.show()  # Show the main window
        self.close()  # Close the landing page

    def close_application(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    landing_page = LandingPage()
    landing_page.show()
    sys.exit(app.exec_())
