from PyQt6.QtWidgets import (
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QVBoxLayout
)


class FinalizacaoWidget(QGroupBox):

    def __init__(self):
        super().__init__("Finalizar Separação")

        self.criar_componentes()
        self.criar_layout()

    # ==================================
    # CRIAÇÃO DOS COMPONENTES
    # ==================================

    def criar_componentes(self):

        self.palete = QLineEdit()
        self.palete.setObjectName("palete")
        self.palete.setPlaceholderText("Número do palete")

        self.montador = QLineEdit()
        self.montador.setObjectName("montador")
        self.montador.setPlaceholderText("Nome do montador")

        self.caixas = QLineEdit()
        self.caixas.setObjectName("caixas")
        self.caixas.setPlaceholderText("Quantidade de caixas")

        self.botao_finalizar = QPushButton("Concluir Separação")
        self.botao_finalizar.setObjectName("botao_finalizar")

    # ==================================
    # CONFIGURAÇÃO DO LAYOUT
    # ==================================

    def criar_layout(self):

        formulario = QFormLayout()

        formulario.addRow(
            QLabel("Palete:"),
            self.palete
        )

        formulario.addRow(
            QLabel("Montador:"),
            self.montador
        )

        formulario.addRow(
            QLabel("Caixas:"),
            self.caixas
        )

        layout = QVBoxLayout()

        layout.addLayout(formulario)
        layout.addStretch()
        layout.addWidget(self.botao_finalizar)

        self.setLayout(layout)