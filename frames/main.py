import csv

from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QScrollArea, QLabel, QMainWindow
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Slot, QThread

from frames.dialog import Dialog
from frames.requisicao import Requisicao


class MainViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.pagina = 1
        self.imagens = []

        self.setWindowTitle('Imagens')
        self.resize(600, 800)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignCenter)

        self.scroll.setWidget(self.container)

        self.button = QPushButton("Carregar imagens")
        self.button.clicked.connect(self.carrega_imagens)

        self.button_csv = QPushButton("Exportar para csv")
        self.button_csv.clicked.connect(self.exportar_csv)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(self.scroll)
        main_layout.addWidget(self.button)
        main_layout.addWidget(self.button_csv)

        self.setCentralWidget(main_widget)

        self.carrega_imagens()

    def carrega_imagens(self):
        self.button.setEnabled(False)
        self.button_csv.setEnabled(False)
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
        self.imagens.append(imagem)
        label = QLabel()
        pixmap = QPixmap()
        pixmap.loadFromData(imagem.photo)
        scaled_pixmap = pixmap.scaled(540, 540)
        label.setPixmap(scaled_pixmap)
        label.setAlignment(Qt.AlignCenter)

        description = QPushButton(imagem.alt)

        description.clicked.connect(lambda: self.abrir_dialog(imagem))

        description.setMinimumWidth(540)
        description.setMaximumWidth(540)

        self.container_layout.addWidget(label)
        self.container_layout.addWidget(description)

    def abrir_dialog(self, imagem):
        dialog = Dialog(imagem)
        dialog.exec()

    @Slot()
    def on_finished(self):
        self.button.setText("Carregar imagens")
        self.button.setEnabled(True)
        self.button_csv.setEnabled(True)

    @Slot()
    def exportar_csv(self):
        with open('dados.csv', 'w', newline='', encoding='utf-8') as file:
            csv_list = [
                [
                    imagem.alt,
                    imagem.width,
                    imagem.height,
                    imagem.photographer,
                    imagem.photographer_url
                ]
                for imagem in self.imagens
            ]
            writer = csv.writer(file)
            writer.writerow(['alt', 'width', 'height', 'photographer', 'photographer_url'])
            writer.writerows(csv_list)
