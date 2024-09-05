import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFrame
)
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QRect

class LandingPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ERROR404 - Lunar Image Processing - Welcome")
        self.setGeometry(100, 100, 1200, 800)  # Adjust size as needed

        # Central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout
        layout = QVBoxLayout(self.central_widget)

        # Set background image
        self.set_background_image('C:/Users/harsh/Documents/Hackathon/hackathon1/Chandrayaan_Image_Optimization-Processing-main/data/raw/bg_img_landingpg.jpg')

        # Transparent black textbox
        self.textbox = QFrame(self)
        self.textbox.setStyleSheet("background-color: rgba(0, 0, 0, 0.3); border-radius: 10px;")
        self.textbox.setLayout(QVBoxLayout())
        
        # Project details
        intro_text = ("<h2 style='color: white;'>ERROR404 - Lunar Image Processing Project</h2>"
                      "<p style='color: white;'>Welcome to the Lunar Image Processing Application. This tool helps in the "
                      "pre-processing, enhancement, denoising, and analysis of lunar images, particularly "
                      "those from Permanently Shadowed Regions (PSR) in lunar craters.</p>"
                      "<h3 style='color: white;'>Steps involved:</h3>"
                      "<ul style='color: white;'>"
                      "<li>Loading Images</li>"
                      "<li>Pre-processing: Noise Reduction, Contrast Adjustment</li>"
                      "<li>Image Enhancement: Histogram Equalization, Retinex</li>"
                      "<li>Denoising: Wavelet Transform, Deep Learning-Based Denoising</li>"
                      "<li>PSR Detection and Analysis</li>"
                      "<li>Saving: Processed images will be saved in the 'processed' directory under 'data'</li>"
                      "</ul>"
                      "<h3 style='color: white;'>Metadata Handling:</h3>"
                      "<p style='color: white;'>The application extracts and saves metadata associated with the images. Metadata includes "
                      "file details such as file name, size, creation time, and modification time. This information is "
                      "stored in JSON format in the 'metadata' directory under 'data', providing insight into the "
                      "processed images and aiding in tracking the processing history.</p>"
                      "<p style='color: white;'>Note: The images used in this application are taken from the image capturing "
                      "done by Chandrayaan 2. You can browse these images at the following link: "
                      "<a href='https://pradan.issdc.gov.in/ch2/protected/browse.xhtml?id=ohrc' style='color: #d3d3d3;'>Chandrayaan 2 OHRC Images</a></p>"
                      "<p style='color: white;'>Click 'Continue' to proceed to the main application or 'Exit' to close.</p>")
        self.intro_label = QLabel(intro_text, self)
        self.intro_label.setAlignment(Qt.AlignCenter)
        self.intro_label.setWordWrap(True)
        self.intro_label.setStyleSheet("font-size: 16px;")  # Adjust font size as needed

        self.textbox.layout().addWidget(self.intro_label)
        layout.addWidget(self.textbox)

        # Continue button
        self.continueButton = QPushButton('Continue', self)
        self.continueButton.setStyleSheet("background-color: purple; color: white;")
        self.continueButton.clicked.connect(self.open_main_gui)
        layout.addWidget(self.continueButton)

        # Exit button
        self.exitButton = QPushButton('Exit', self)
        self.exitButton.setStyleSheet("background-color: purple; color: white;")
        self.exitButton.clicked.connect(self.close_application)
        layout.addWidget(self.exitButton)

    def set_background_image(self, image_path):
        # Set background image
        background_pixmap = QPixmap(image_path)
        scaled_pixmap = background_pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette = self.palette()
        palette.setBrush(self.backgroundRole(), QBrush(scaled_pixmap))
        self.setPalette(palette)

    def open_main_gui(self):
        from gui import MainWindow
        self.main_window = MainWindow()  # Create an instance of MainWindow from gui.py
        self.main_window.show()  # Show the main window
        self.close()  # Close the landing page

    def close_application(self):
        self.close()

    def resizeEvent(self, event):
        # Resize background image on window resize
        self.set_background_image('C:/Users/harsh/Documents/Hackathon/hackathon1/Chandrayaan_Image_Optimization-Processing-main/data/raw/bg_img_landingpg.jpg')
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    landing_page = LandingPage()
    landing_page.show()
    sys.exit(app.exec_())
