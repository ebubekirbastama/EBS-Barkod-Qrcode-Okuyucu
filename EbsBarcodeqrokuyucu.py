import sys
from pyzbar.pyzbar import decode
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

class EBSBarkodOkuyucu(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):

        self.setWindowTitle('EBS Barkod Okuyucu')

        # Modern bir gradyan arka plan rengi
        self.setStyleSheet("""
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(85, 182, 224, 255), stop:1 rgba(0, 120, 255, 255));
            font-family: Arial, sans-serif;
        """)

        layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.barkod_label = QLabel('Barkod Verisi Burada Gösterilecek', self)
        self.barkod_label.setAlignment(Qt.AlignCenter)
        self.barkod_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(self.barkod_label)


        self.select_button = QPushButton('Barkod Resmi Seç', self)
        self.select_button.setStyleSheet("background-color: #5c6bc0; color: white; border-radius: 5px; padding: 10px 20px; font-size: 16px;")
        self.select_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_button)


        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Veya Barkod URL ya da Dosya Yolu Girin")
        self.input_field.setStyleSheet("padding: 10px; font-size: 16px; border: 2px solid #5c6bc0; border-radius: 5px; margin-top: 20px;")
        self.input_field.returnPressed.connect(self.read_barcode_from_input)
        layout.addWidget(self.input_field)


        self.setLayout(layout)
        self.setGeometry(100, 100, 500, 400)
        self.show()

    def select_file(self):

        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, 'Barkod Resmi Seç', '', 'PNG Files (*.png);;All Files (*)', options=options)

        if file:
            self.barkod_label.setText(file)
            self.process_image(file)

    def process_image(self, file_path):

        image = Image.open(file_path)

        barkodlar = decode(image)


        if barkodlar:
            for barkod in barkodlar:

                barkod_verisi = barkod.data.decode('utf-8')

                self.input_field.setText(f'Barkod Verisi: {barkod_verisi}')
        else:
            self.barkod_label.setText('Barkod Bulunamadı')

        pixmap = QPixmap(file_path)
        self.image_label.setPixmap(pixmap.scaled(400, 300, Qt.KeepAspectRatio))

    def read_barcode_from_input(self):

        file_path = self.input_field.text()
        if file_path:
            self.process_image(file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EBSBarkodOkuyucu()
    sys.exit(app.exec_())
