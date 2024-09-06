import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QMessageBox, QTextEdit, QProgressBar, QFileDialog
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from preprocessing import preprocess_and_save
from psr_mapping import map_psr_and_save
from advanced_denoising import denoise_and_save
from enhancement import enhance_and_save

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lunar Image Processing")
        self.setGeometry(100, 100, 1200, 800)

        # Main container widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Image display area (80% of the height)
        self.image_frame = QFrame(self)
        self.image_frame.setFrameShape(QFrame.Box)
        self.image_frame.setFrameShadow(QFrame.Sunken)
        self.image_frame.setStyleSheet("background-color: #2E2E2E; border: 2px solid #8A2BE2;")
        self.image_layout = QVBoxLayout(self.image_frame)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_layout.addWidget(self.image_label)
        self.layout.addWidget(self.image_frame, 8)

        # Metadata display area (20% of the height)
        self.metadata_frame = QFrame(self)
        self.metadata_frame.setFrameShape(QFrame.Box)
        self.metadata_frame.setFrameShadow(QFrame.Sunken)
        self.metadata_frame.setStyleSheet("background-color: #1E1E1E; border: 2px solid #8A2BE2;")
        self.metadata_layout = QVBoxLayout(self.metadata_frame)
        self.metadata_display = QTextEdit(self)
        self.metadata_display.setReadOnly(True)
        self.metadata_display.setStyleSheet("color: white; background-color: #1E1E1E; border: none;")
        self.metadata_layout.addWidget(self.metadata_display)
        self.layout.addWidget(self.metadata_frame, 2)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.upload_button = QPushButton("Upload Image", self)
        self.upload_button.setStyleSheet("background-color: #8A2BE2; color: white; font-weight: bold;")
        self.upload_button.clicked.connect(self.upload_image)
        self.button_layout.addWidget(self.upload_button)

        self.process_button = QPushButton("Process Image", self)
        self.process_button.setStyleSheet("background-color: #8A2BE2; color: white; font-weight: bold;")
        self.process_button.clicked.connect(self.process_image)
        self.button_layout.addWidget(self.process_button)

        self.export_button = QPushButton("Export Image", self)
        self.export_button.setStyleSheet("background-color: #8A2BE2; color: white; font-weight: bold;")
        self.export_button.clicked.connect(self.export_image)
        self.button_layout.addWidget(self.export_button)

        self.layout.addLayout(self.button_layout)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet("QProgressBar::chunk {background-color: #8A2BE2;}")
        self.layout.addWidget(self.progress_bar)

        # Initialize file paths
        self.file_path = None
        self.metadata_path = None
        self.processed_psr_mapped_path = None  # Use this to store PSR mapped image path

    def upload_image(self):
        """
        Opens a file dialog to select an image file and displays it.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose an Image File", "", "Image Files (*.png; *.jpg; *.jpeg; *.bmp; *.tiff);;All Files (*)", options=options)
        if file_name:
            self.file_path = file_name
            self.show_image(file_name)

    def show_image(self, file_path):
        """
        Displays the selected image in the GUI.
        """
        pixmap = QPixmap(file_path)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def display_metadata(self, metadata_path):
        """
        Displays metadata in the GUI.
        """
        with open(metadata_path, 'r') as f:
            metadata = f.read()
        self.metadata_display.setPlainText(metadata)

    def process_image(self):
        """
        Processes the selected image and updates the GUI with the results.
        """
        if not self.file_path:
            QMessageBox.warning(self, "Error", "No image file selected!")
            return

        self.progress_bar.setValue(0)
        processed_image_path = preprocess_and_save(self.file_path)
        self.progress_bar.setValue(30)
        self.processed_psr_mapped_path, metadata_path = map_psr_and_save(processed_image_path, self.file_path)
        self.progress_bar.setValue(60)
        denoised_image_path = denoise_and_save(self.processed_psr_mapped_path)
        self.progress_bar.setValue(90)
        enhance_and_save(denoised_image_path)
        self.progress_bar.setValue(100)
        self.show_image(self.processed_psr_mapped_path)  # Show the PSR mapped image
        self.display_metadata(metadata_path)
        QMessageBox.information(self, "Success", "Image processing completed!")

    def export_image(self):
        """
        Opens a file dialog to save the PSR mapped image.
        """
        if not self.processed_psr_mapped_path:
            QMessageBox.warning(self, "Error", "No processed image to export!")
            return

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image File", "", "Image Files (*.png; *.jpg);;All Files (*)", options=options)
        if file_name:
            pixmap = QPixmap(self.processed_psr_mapped_path)
            pixmap.save(file_name)
            QMessageBox.information(self, "Success", f"Image exported to {file_name}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
