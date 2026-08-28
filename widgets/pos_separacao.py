from PyQt6.QtWidgets import (
    QGroupBox,
    QLabel,
    QCheckBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)


class PosSeparacaoWidget(QGroupBox):

    def __init__(self):
        super().__init__("Pós-separação")

        self.lote_selecionado = None

        self.criar_componentes()
        self.criar_layout()

    # =========================================================
    # CRIAÇÃO DOS COMPONENTES
    # =========================================================

    def criar_componentes(self):

        self.lbl_lote = QLabel(
            "Nenhum lote selecionado"
        )

        self.lbl_lote.setStyleSheet(
            "font-weight: bold; font-size: 14px;"
        )

        # -----------------------------------------------------
        # CHECKBOXES
        # -----------------------------------------------------

        self.faturado = QCheckBox(
            "Faturado"
        )

        self.faturado.setObjectName(
            "faturado"
        )

        self.embarcado = QCheckBox(
            "Embarcado"
        )

        self.embarcado.setObjectName(
            "embarcado"
        )

        self.pre_autorizacao = QCheckBox(
            "Pré-autorização"
        )

        self.pre_autorizacao.setObjectName(
            "pre_autorizacao"
        )

        self.notas_impressas = QCheckBox(
            "Notas fiscais"
        )

        self.notas_impressas.setObjectName(
            "notas_impressas"
        )

        # -----------------------------------------------------
        # BOTÃO
        # -----------------------------------------------------

        self.botao_salvar = QPushButton(
            "Salvar Pós-separação"
        )

        self.botao_salvar.setObjectName(
            "botao_salvar_pos"
        )

        self.botao_salvar.setEnabled(
            False
        )

    # =========================================================
    # LAYOUT
    # =========================================================

    def criar_layout(self):

        layout_principal = QVBoxLayout()

        layout_principal.addWidget(
            self.lbl_lote
        )

        linha_checkboxes = QHBoxLayout()

        linha_checkboxes.addWidget(
            self.faturado
        )

        linha_checkboxes.addWidget(
            self.embarcado
        )

        linha_checkboxes.addWidget(
            self.pre_autorizacao
        )

        linha_checkboxes.addWidget(
            self.notas_impressas
        )

        layout_principal.addLayout(
            linha_checkboxes
        )

        layout_principal.addWidget(
            self.botao_salvar
        )

        self.setLayout(
            layout_principal
        )

    # =========================================================
    # SELECIONAR LOTE
    # =========================================================

    def selecionar_lote(
        self,
        lote,
        faturado=0,
        embarcado=0,
        pre_autorizacao=0,
        notas_impressas=0
    ):

        self.lote_selecionado = lote

        self.lbl_lote.setText(
            f"Lote selecionado: {lote}"
        )

        self.faturado.setChecked(
            bool(faturado)
        )

        self.embarcado.setChecked(
            bool(embarcado)
        )

        self.pre_autorizacao.setChecked(
            bool(pre_autorizacao)
        )

        self.notas_impressas.setChecked(
            bool(notas_impressas)
        )

        self.botao_salvar.setEnabled(
            True
        )

    # =========================================================
    # LIMPAR SELEÇÃO
    # =========================================================

    def limpar(self):

        self.lote_selecionado = None

        self.lbl_lote.setText(
            "Nenhum lote selecionado"
        )

        self.faturado.setChecked(
            False
        )

        self.embarcado.setChecked(
            False
        )

        self.pre_autorizacao.setChecked(
            False
        )

        self.notas_impressas.setChecked(
            False
        )

        self.botao_salvar.setEnabled(
            False
        )

    # =========================================================
    # PEGAR DADOS
    # =========================================================

    def obter_dados(self):

        return {
            "lote": self.lote_selecionado,

            "faturado":
                int(self.faturado.isChecked()),

            "embarcado":
                int(self.embarcado.isChecked()),

            "pre_autorizacao":
                int(self.pre_autorizacao.isChecked()),

            "notas_impressas":
                int(self.notas_impressas.isChecked())
        }