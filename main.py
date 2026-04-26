import sys

import requests
from PySide6.QtWidgets import QPushButton, QWidget, QApplication, QVBoxLayout, QScrollArea, QLabel, QMainWindow
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Slot, QObject, QThread, Signal

from service import Service


class Requisicao(QObject):
    finalizado = Signal()
    atualizar = Signal(object)

    def __init__(self, pagina):
        super().__init__()
        self.pagina = pagina

    @Slot()
    def requisicao_lenta(self):
        self.carrega_imagens()
        self.finalizado.emit()

    def carrega_imagens(self):  # TODO: Fazer novos métodos com novas camadas para chamadas
        service = Service(pagina=self.pagina)
        request = service.get_requisicao()

        for imagem in request['photos']:
            response = requests.get(imagem['src']['large'])  # TODO: Melhorar fluxo de chamadas

            imagem = {
                "label": response.content,
                "description": imagem['alt']
            }
            self.atualizar.emit(imagem)


class MainViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.pagina = 1

        self.setWindowTitle('Imagens')
        self.resize(800, 600)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignTop)

        self.scroll.setWidget(self.container)

        self.button = QPushButton("Carregar imagens")
        self.button.clicked.connect(self.start_thread)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(self.scroll)
        main_layout.addWidget(self.button)

        self.setCentralWidget(main_widget)

    def start_thread(self):
        self.button.setEnabled(False)

        self.thread = QThread()
        self.requisicao = Requisicao(pagina=self.pagina)

        self.requisicao.moveToThread(self.thread)

        self.thread.started.connect(self.requisicao.requisicao_lenta)
        self.requisicao.finalizado.connect(self.thread.quit)
        self.requisicao.finalizado.connect(self.requisicao.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.requisicao.atualizar.connect(self.update_label)
        self.thread.finished.connect(self.on_finished)

        self.thread.start()

        self.pagina += 1

    @Slot(object)
    def update_label(self, imagem):
        label = QLabel()
        pixmap = QPixmap()
        pixmap.loadFromData(imagem['label'])
        scaled_pixmap = pixmap.scaled(800, 600)
        label.setPixmap(scaled_pixmap)

        description = QLabel(imagem['description'])

        self.container_layout.addWidget(label)
        self.container_layout.addWidget(description)

    @Slot()
    def on_finished(self):
        self.button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainViewer()
    window.show()
    sys.exit(app.exec())
