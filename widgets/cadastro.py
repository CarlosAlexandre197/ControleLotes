from PyQt6.QtWidgets import (
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QVBoxLayout
)


class CadastroWidget(QGroupBox):

    def __init__(self):
        super().__init__("Cadastro do Lote")

        self.criar_componentes()
        self.criar_layout()


    def criar_componentes(self):

        self.lote = QLineEdit()
        self.lote.setObjectName("lote")
        self.lote.setPlaceholderText("Número do lote")

        self.quantidade = QLineEdit()
        self.quantidade.setObjectName("quantidade")
        self.quantidade.setPlaceholderText("Quantidade")

        self.cartoes = QLineEdit()
        self.cartoes.setObjectName("cartoes")
        self.cartoes.setPlaceholderText("Cartões")

        self.cancelados = QLineEdit()
        self.cancelados.setObjectName("cancelados")
        self.cancelados.setPlaceholderText("Cancelados")

        self.botao_salvar = QPushButton("Cadastrar Lote")
        self.botao_salvar.setObjectName("botao_salvar")


    def criar_layout(self):

        formulario = QFormLayout()

        formulario.addRow(QLabel("Lote:"), self.lote)
        formulario.addRow(QLabel("Quantidade:"), self.quantidade)
        formulario.addRow(QLabel("Cartões:"), self.cartoes)
        formulario.addRow(QLabel("Cancelados:"), self.cancelados)

        layout = QVBoxLayout()

        layout.addLayout(formulario)
        layout.addStretch()
        layout.addWidget(self.botao_salvar)

        self.setLayout(layout)