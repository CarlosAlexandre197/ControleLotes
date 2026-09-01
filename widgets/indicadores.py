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

    # ==================================
    # CRIAÇÃO DOS COMPONENTES
    # ==================================

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

    # ==================================
    # CRIA UM CARTÃO DE INDICADOR
    # ==================================

    def criar_indicador(self, titulo, valor):

        frame = QFrame()

        frame.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        layout = QVBoxLayout()

        label_titulo = QLabel(titulo)

        label_titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        label_valor = QLabel(valor)

        label_valor.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        label_valor.setObjectName(
            f"valor_{titulo.lower().replace(' ', '_')}"
        )

        layout.addWidget(
            label_titulo
        )

        layout.addWidget(
            label_valor
        )

        frame.setLayout(
            layout
        )

        frame.valor = label_valor

        return frame

    # ==================================
    # LAYOUT
    # ==================================

    def criar_layout(self):

        layout_principal = QVBoxLayout()

        # ----------------------------------
        # PRIMEIRA LINHA
        # ----------------------------------

        linha1 = QHBoxLayout()

        linha1.addWidget(
            self.lbl_total_lotes
        )

        linha1.addWidget(
            self.lbl_total_pedidos
        )

        linha1.addWidget(
            self.lbl_total_caixas
        )

        # ----------------------------------
        # SEGUNDA LINHA
        # ----------------------------------

        linha2 = QHBoxLayout()

        linha2.addWidget(
            self.lbl_pendentes
        )

        linha2.addWidget(
            self.lbl_finalizados
        )

        linha2.addWidget(
            self.lbl_total_omni
        )

        # ----------------------------------
        # TERCEIRA LINHA
        # ----------------------------------

        linha3 = QHBoxLayout()

        linha3.addWidget(
            self.lbl_total_geral
        )

        # ----------------------------------
        # ADICIONAR AO LAYOUT PRINCIPAL
        # ----------------------------------

        layout_principal.addLayout(
            linha1
        )

        layout_principal.addLayout(
            linha2
        )

        layout_principal.addLayout(
            linha3
        )

        self.setLayout(
            layout_principal
        )

    # ==================================
    # ATUALIZAÇÃO DOS INDICADORES
    # ==================================

    def atualizar(
        self,
        total_lotes,
        total_pedidos,
        total_caixas,
        pendentes,
        finalizados,
        total_omni=0
    ):

        total_geral = (
            total_pedidos
            + total_omni
        )

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