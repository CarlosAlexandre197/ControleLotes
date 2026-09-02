from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox
)


class EditarLoteDialog(QDialog):

    def __init__(self, dados_lote, parent=None):
        super().__init__(parent)

        self.dados_lote = dados_lote

        self.setWindowTitle("Editar Lote")
        self.setFixedWidth(400)

        self.criar_componentes()
        self.carregar_dados()
        self.criar_layout()
        self.conectar_eventos()

    def criar_componentes(self):

        self.lote = QLineEdit()
        self.quantidade = QLineEdit()
        self.cartoes = QLineEdit()
        self.cancelados = QLineEdit()

        self.quantidade_final = QLineEdit()
        self.quantidade_final.setReadOnly(True)

        self.palete = QLineEdit()
        self.montador = QLineEdit()
        self.caixas = QLineEdit()

        self.botao_salvar = QPushButton("Salvar Alterações")
        self.botao_cancelar = QPushButton("Cancelar")

    def carregar_dados(self):

        # Ordem das colunas da tabela:
        # 0 Lote
        # 1 Quantidade
        # 2 Cartões
        # 3 Cancelados
        # 4 Quantidade Final
        # 5 Palete
        # 6 Montador
        # 7 Caixas
        # 8 Status

        self.lote.setText(str(self.dados_lote[0]))
        self.quantidade.setText(str(self.dados_lote[1]))
        self.cartoes.setText(str(self.dados_lote[2]))
        self.cancelados.setText(str(self.dados_lote[3]))
        self.quantidade_final.setText(str(self.dados_lote[4]))
        self.palete.setText(str(self.dados_lote[5] or ""))
        self.montador.setText(str(self.dados_lote[6] or ""))
        self.caixas.setText(str(self.dados_lote[7] or ""))

        # Guardamos o lote original para o UPDATE
        self.lote_original = str(self.dados_lote[0])

    def criar_layout(self):

        formulario = QFormLayout()

        formulario.addRow("Lote:", self.lote)
        formulario.addRow("Quantidade:", self.quantidade)
        formulario.addRow("Cartões:", self.cartoes)
        formulario.addRow("Cancelados:", self.cancelados)
        formulario.addRow("Quantidade Final:", self.quantidade_final)
        formulario.addRow("Palete:", self.palete)
        formulario.addRow("Montador:", self.montador)
        formulario.addRow("Caixas:", self.caixas)

        botoes = QHBoxLayout()

        botoes.addWidget(self.botao_salvar)
        botoes.addWidget(self.botao_cancelar)

        layout = QVBoxLayout()

        layout.addLayout(formulario)
        layout.addLayout(botoes)

        self.setLayout(layout)

    def conectar_eventos(self):

        self.quantidade.textChanged.connect(
            self.calcular_quantidade_final
        )

        self.cartoes.textChanged.connect(
            self.calcular_quantidade_final
        )

        self.cancelados.textChanged.connect(
            self.calcular_quantidade_final
        )

        self.botao_salvar.clicked.connect(
            self.salvar
        )

        self.botao_cancelar.clicked.connect(
            self.reject
        )

    def calcular_quantidade_final(self):

        try:
            quantidade = int(self.quantidade.text() or 0)
            cartoes = int(self.cartoes.text() or 0)
            cancelados = int(self.cancelados.text() or 0)

            resultado = quantidade - cartoes - cancelados

            self.quantidade_final.setText(str(resultado))

        except ValueError:

            self.quantidade_final.setText("0")

    def salvar(self):

        lote = self.lote.text().strip()
        quantidade_texto = self.quantidade.text().strip()
        cartoes_texto = self.cartoes.text().strip()
        cancelados_texto = self.cancelados.text().strip()
        caixas_texto = self.caixas.text().strip()

        if not lote:
            QMessageBox.warning(
                self,
                "Atenção",
                "Informe o número do lote."
            )
            return

        try:
            quantidade = int(quantidade_texto)
            cartoes = int(cartoes_texto or 0)
            cancelados = int(cancelados_texto or 0)

        except ValueError:
            QMessageBox.warning(
                self,
                "Atenção",
                "Quantidade, cartões e cancelados devem ser números."
            )
            return

        if quantidade <= 0:
            QMessageBox.warning(
                self,
                "Atenção",
                "A quantidade deve ser maior que zero."
            )
            return

        if cartoes < 0 or cancelados < 0:
            QMessageBox.warning(
                self,
                "Atenção",
                "Cartões e cancelados não podem ser negativos."
            )
            return

        quantidade_final = quantidade - cartoes - cancelados

        if quantidade_final < 0:
            QMessageBox.warning(
                self,
                "Erro",
                "Quantidade final não pode ser negativa."
            )
            return

        if caixas_texto:
            try:
                caixas = int(caixas_texto)

                if caixas < 0:
                    raise ValueError

            except ValueError:
                QMessageBox.warning(
                    self,
                    "Atenção",
                    "Caixas deve ser um número igual ou maior que zero."
                )
                return
        else:
            caixas = 0

        self.resultado = {
            "lote_original": self.lote_original,
            "lote": lote,
            "quantidade": quantidade,
            "cartoes": cartoes,
            "cancelados": cancelados,
            "quantidade_final": quantidade_final,
            "palete": self.palete.text().strip(),
            "montador": self.montador.text().strip(),
            "caixas": caixas
        }

        self.accept()