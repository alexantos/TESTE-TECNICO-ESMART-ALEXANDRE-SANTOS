import sys
from time import sleep

import requests
from PySide6.QtWidgets import QPushButton, QWidget, QApplication, QVBoxLayout, QScrollArea, QLabel, QMainWindow
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Slot

from service import Service


class MainViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Imagens')
        self.resize(800, 600)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignTop)

        self.scroll.setWidget(self.container)

        self.add_button = QPushButton("Carregar imagens")
        self.add_button.clicked.connect(self.carrega_imagem_click)

        self.carrega_imagens()

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(self.scroll)
        main_layout.addWidget(self.add_button)

        self.setCentralWidget(main_widget)


    @Slot()
    def carrega_imagem_click(self):
        self.carrega_imagens(pagina=2)
        # sleep(10)

    def carrega_imagens(self, pagina=1): #TODO: Fazer novos métodos com novas camadas para chamadas
        service = Service(pagina=pagina)
        request = service.get_requisicao()

        for imagem in request['photos']:
            label = QLabel()
            response = requests.get(imagem['src']['large']) #TODO: Melhorar fluxo de chamadas
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            scaled_pixmap = pixmap.scaled(800, 600)
            label.setPixmap(scaled_pixmap)
            description = QLabel(imagem['alt'])

            self.container_layout.addWidget(label)
            self.container_layout.addWidget(description)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainViewer()
    window.show()
    sys.exit(app.exec())
