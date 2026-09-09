from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame
)

from PyQt6.QtCore import Qt


class IndicadoresWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.criar_componentes()
        self.criar_layout()
        self.aplicar_estilo()

    def criar_componentes(self):

        self.lbl_total_lotes = self.criar_indicador(
            "TOTAL DE LOTES",
            "0"
        )

        self.lbl_total_pedidos = self.criar_indicador(
            "TOTAL DE PEDIDOS",
            "0"
        )

        self.lbl_total_caixas = self.criar_indicador(
            "TOTAL DE CAIXAS",
            "0"
        )

        self.lbl_pendentes = self.criar_indicador(
            "PENDENTES",
            "0"
        )

        self.lbl_finalizados = self.criar_indicador(
            "FINALIZADOS",
            "0"
        )

        self.lbl_total_omni = self.criar_indicador(
            "TOTAL OMNICHANNEL",
            "0"
        )

        self.lbl_total_geral = self.criar_indicador(
            "TOTAL GERAL DE PEDIDOS",
            "0"
        )

    def criar_indicador(self, titulo, valor):

        frame = QFrame()
        frame.setObjectName("card")

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(3)

        label_titulo = QLabel(titulo)
        label_titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        label_valor = QLabel(valor)
        label_valor.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        label_valor.setObjectName("valor")

        layout.addWidget(label_titulo)
        layout.addWidget(label_valor)

        frame.setLayout(layout)

        frame.valor = label_valor

        return frame

    def criar_layout(self):

        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(8)

        linha1 = QHBoxLayout()
        linha1.setSpacing(8)

        linha1.addWidget(self.lbl_total_lotes)
        linha1.addWidget(self.lbl_total_pedidos)
        linha1.addWidget(self.lbl_total_caixas)

        linha2 = QHBoxLayout()
        linha2.setSpacing(8)

        linha2.addWidget(self.lbl_pendentes)
        linha2.addWidget(self.lbl_finalizados)
        linha2.addWidget(self.lbl_total_omni)

        linha3 = QHBoxLayout()
        linha3.setSpacing(8)

        linha3.addWidget(self.lbl_total_geral)

        layout_principal.addLayout(linha1)
        layout_principal.addLayout(linha2)
        layout_principal.addLayout(linha3)

        self.setLayout(layout_principal)

    def aplicar_estilo(self):

        self.setStyleSheet("""
            QFrame#card {
                background-color: white;
                border: 1px solid #d9d9d9;
                border-radius: 8px;
            }

            QFrame#card:hover {
                border: 1px solid #1976d2;
            }

            QFrame#card QLabel {
                border: none;
                background: transparent;
            }

            QFrame#card QLabel#valor {
                font-size: 24px;
                font-weight: bold;
                color: #1976d2;
                padding: 3px;
            }
        """)

    def atualizar(
        self,
        total_lotes,
        total_pedidos,
        total_caixas,
        pendentes,
        finalizados,
        total_omni=0
    ):

        total_geral = total_pedidos + total_omni

        self.lbl_total_lotes.valor.setText(
            str(total_lotes)
        )

        self.lbl_total_pedidos.valor.setText(
            str(total_pedidos)
        )

        self.lbl_total_caixas.valor.setText(
            str(total_caixas)
        )

        self.lbl_pendentes.valor.setText(
            str(pendentes)
        )

        self.lbl_finalizados.valor.setText(
            str(finalizados)
        )

        self.lbl_total_omni.valor.setText(
            str(total_omni)
        )

        self.lbl_total_geral.valor.setText(
            str(total_geral)
        )