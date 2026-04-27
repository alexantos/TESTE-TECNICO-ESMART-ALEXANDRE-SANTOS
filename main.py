import sys

import requests
from PySide6.QtWidgets import QPushButton, QWidget, QApplication, QVBoxLayout, QScrollArea, QLabel, QMainWindow, QDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Slot, QObject, QThread, Signal

from service import Service


class Dialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Detalhe da foto")
        layout = QVBoxLayout()
        self.alt = QLabel(data['alt'])
        self.width = QLabel(str(data['width']))
        self.height = QLabel(str(data['height']))
        self.photographer = QLabel(data['photographer'])
        self.photographer_url = QLabel(data['photographer_url'])
        # self.label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.alt)
        layout.addWidget(self.width)
        layout.addWidget(self.height)
        layout.addWidget(self.photographer)
        layout.addWidget(self.photographer_url)
        self.setLayout(layout)


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
                "id": imagem['id'],
                "photo": response.content,
                "alt": imagem['alt'],
                "width": imagem['width'],
                "height": imagem['height'],
                "photographer": imagem['photographer'],
                "photographer_url": imagem['photographer_url'],
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
        self.button.setText('Carregando...')

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
        pixmap.loadFromData(imagem['photo'])
        scaled_pixmap = pixmap.scaled(800, 600)
        label.setPixmap(scaled_pixmap)

        description = QPushButton(imagem['alt'])

        description.clicked.connect(lambda: self.abrir_dialog(imagem))

        self.container_layout.addWidget(label)
        self.container_layout.addWidget(description)

    def abrir_dialog(self, imagem):
        dialog = Dialog(imagem)
        dialog.exec()

    @Slot()
    def on_finished(self):
        self.button.setText("Carregar imagens")
        self.button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainViewer()
    window.show()
    sys.exit(app.exec())
