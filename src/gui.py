import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QProgressBar
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
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

        # Central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout
        layout = QVBoxLayout(self.central_widget)

        # Add image display
        self.imageLabel = QLabel(self)
        self.imageLabel.setFrameShape(QFrame.Box)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.imageLabel)

        # Add control buttons in a horizontal layout
        buttonLayout = QHBoxLayout()
        layout.addLayout(buttonLayout)

        self.loadButton = QPushButton('Load Image', self)
        self.loadButton.setToolTip('Click to load an image')
        self.loadButton.clicked.connect(self.load_image)
        buttonLayout.addWidget(self.loadButton)

        self.processButton = QPushButton('Process Image', self)
        self.processButton.setToolTip('Click to process the loaded image')
        self.processButton.clicked.connect(self.process_image)
        buttonLayout.addWidget(self.processButton)

        # Add a status bar
        self.statusBar = self.statusBar()

        # Add a progress bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)

        self.model = None  # Placeholder for AI model (can be replaced with actual model later)

    def load_image(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "Images (*.png *.jpg);;All Files (*)", options=options)
        if filePath:
            self.image = cv2.imread(filePath, cv2.IMREAD_GRAYSCALE)
            pixmap = QPixmap(filePath)
            self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.loaded_image_path = filePath  # Store the loaded image path for later use
            self.statusBar.showMessage("Image loaded successfully.")

    def process_image(self):
        if hasattr(self, 'image'):
            try:
                self.progressBar.setValue(20)
                enhanced_image = enhance_image(self.image)
                self.progressBar.setValue(50)
                # Apply denoising
                denoised_image = deep_learning_denoising(enhanced_image, self.model)
                self.progressBar.setValue(80)

                # Path to save the enhanced image in the 'processed' directory under 'data'
                base_dir = os.path.dirname(os.path.abspath(__file__))
                processed_dir = os.path.join(base_dir, '..', 'data', 'processed')
                os.makedirs(processed_dir, exist_ok=True)

                # Save the enhanced image in the 'processed' directory
                base_name = os.path.basename(self.loaded_image_path)
                enhanced_image_path = os.path.join(processed_dir, f"{os.path.splitext(base_name)[0]}_enhanced.png")
                cv2.imwrite(enhanced_image_path, denoised_image)
                
                # Display the enhanced image
                pixmap = QPixmap(enhanced_image_path)
                self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.progressBar.setValue(100)
                self.statusBar.showMessage("Image processing completed successfully.")

            except Exception as e:
                self.progressBar.setValue(0)
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")
                self.statusBar.showMessage("Error during image processing.")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
