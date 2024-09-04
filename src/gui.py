# src/gui.py
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QFileDialog, QMessageBox, QWidget, QProgressBar, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from preprocessing import preprocess_and_save
from psr_mapping import map_psr_and_save
from advanced_denoising import denoise_and_save
from enhancement import enhance_and_save
from segmentation import segment_image  # Import the segmentation function
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lunar Image Processing")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.upload_button = QPushButton("Upload Image", self)
        self.upload_button.clicked.connect(self.upload_image)
        self.layout.addWidget(self.upload_button)

        self.process_button = QPushButton("Process Image", self)
        self.process_button.clicked.connect(self.process_image)
        self.layout.addWidget(self.process_button)

        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        self.export_dir_input = QLineEdit(self)
        self.export_dir_input.setPlaceholderText("Export Directory (optional)")
        self.layout.addWidget(self.export_dir_input)

        self.file_path = None

    def upload_image(self):
        """
        Opens a file dialog to select an image file and displays it.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose an Image File", "", "Image Files (*.png; *.jpg);;All Files (*)", options=options)
        if file_name:
            self.file_path = file_name
            self.show_image(file_name)

    def show_image(self, file_path):
        """
        Displays the selected image in the GUI.
        """
        pixmap = QPixmap(file_path)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def process_image(self):
        """
        Processes the selected image and updates the GUI with the results.
        """
        if not self.file_path:
            QMessageBox.warning(self, "Error", "No image file selected!")
            return

        export_dir = self.export_dir_input.text().strip()

        self.progress_bar.setValue(0)
        processed_image_path = preprocess_and_save(self.file_path)
        self.progress_bar.setValue(25)
        psr_mapped_image_path = map_psr_and_save(processed_image_path, self.file_path, export_dir)  # Use the original image as the lunar map
        self.progress_bar.setValue(50)
        denoised_image_path = denoise_and_save(psr_mapped_image_path)
        self.progress_bar.setValue(75)
        enhanced_image_path = enhance_and_save(denoised_image_path)
        self.progress_bar.setValue(90)

        # Add segmentation step
        segmented_image_path = os.path.join(export_dir, 'segmented_image.png')
        segment_image(enhanced_image_path, segmented_image_path)
        
        self.progress_bar.setValue(100)
        self.show_image(segmented_image_path)
        QMessageBox.information(self, "Success", "Image processing and segmentation completed!")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
