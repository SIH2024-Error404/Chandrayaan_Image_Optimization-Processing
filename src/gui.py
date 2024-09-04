from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
from preprocessing import reduce_noise, adjust_contrast, crop_and_align
from enhancement import enhance_image
from advanced_denoising import apply_wavelet_denoising, deep_learning_denoising
from psr_mapping import detect_psr_regions
from analysis import calculate_snr, extract_features, compare_images

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lunar Image Processing")
        self.setGeometry(100, 100, 800, 600)

        # Add buttons and labels for each functionality
        self.loadButton = QPushButton('Load Image', self)
        self.loadButton.clicked.connect(self.load_image)
        self.loadButton.move(50, 50)

        self.processButton = QPushButton('Process Image', self)
        self.processButton.clicked.connect(self.process_image)
        self.processButton.move(50, 100)

        self.imageLabel = QLabel(self)
        self.imageLabel.move(200, 50)

        self.model = None  # Placeholder for AI model (can be replaced with actual model later)

    def load_image(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "Images (*.png *.jpg);;All Files (*)", options=options)
        if filePath:
            self.image = cv2.imread(filePath, cv2.IMREAD_GRAYSCALE)
            pixmap = QPixmap(filePath)
            self.imageLabel.setPixmap(pixmap)

    def process_image(self):
        # Apply preprocessing, enhancement, and analysis steps here
        if hasattr(self, 'image'):
            try:
                enhanced_image = enhance_image(self.image)
                # Apply denoising
                denoised_image = deep_learning_denoising(enhanced_image, self.model)
                
                # Save or display the enhanced image
                cv2.imwrite('enhanced_image.png', denoised_image)
                pixmap = QPixmap('enhanced_image.png')
                self.imageLabel.setPixmap(pixmap)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()