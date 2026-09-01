from PyQt6.QtCore import pyqtSignal
from datetime import datetime

from PyQt6.QtWidgets import (
    QGroupBox,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QAbstractItemView,
    QHeaderView,
    QMessageBox
)

from banco import (
    salvar_omni,
    buscar_omni_do_dia,
    atualizar_omni,
    excluir_omni
)


class OmniWidget(QGroupBox):
    
    total_alterado = pyqtSignal()

    def __init__(self):
        super().__init__("OmniChannel")

        self.criar_componentes()
        self.criar_layout()
        self.configurar_tabela()
        self.conectar_eventos()

    # =========================================================
    # CRIAÇÃO DOS COMPONENTES
    # =========================================================

    def criar_componentes(self):

        self.quantidade = QLineEdit()

        self.quantidade.setObjectName(
            "omni_quantidade"
        )

        self.quantidade.setPlaceholderText(
            "Quantidade de pedidos"
        )

        self.botao_adicionar = QPushButton(
            "Adicionar"
        )

        self.botao_adicionar.setObjectName(
            "botao_add_omni"
        )

        self.botao_editar = QPushButton(
            "Editar"
        )

        self.botao_editar.setObjectName(
            "botao_editar_omni"
        )

        self.botao_excluir = QPushButton(
            "Excluir"
        )

        self.botao_excluir.setObjectName(
            "botao_excluir_omni"
        )

        self.lbl_total = QLabel(
            "Total OmniChannel: 0"
        )

        self.lbl_total.setObjectName(
            "lbl_total_omni"
        )

        self.tabela = QTableWidget()

        self.tabela.setObjectName(
            "tabela_omni"
        )

    # =========================================================
    # CONFIGURAÇÃO DA TABELA
    # =========================================================

    def configurar_tabela(self):

        self.tabela.setColumnCount(3)

        self.tabela.setHorizontalHeaderLabels([
            "ID",
            "Quantidade",
            "Hora"
        ])

        self.tabela.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.tabela.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.tabela.verticalHeader().setVisible(
            False
        )

        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tabela.setAlternatingRowColors(
            True
        )

    # =========================================================
    # LAYOUT
    # =========================================================

    def criar_layout(self):

        entrada_layout = QHBoxLayout()

        entrada_layout.addWidget(
            self.quantidade
        )

        entrada_layout.addWidget(
            self.botao_adicionar
        )

        entrada_layout.addWidget(
            self.botao_editar
        )

        entrada_layout.addWidget(
            self.botao_excluir
        )

        layout = QVBoxLayout()

        layout.addLayout(
            entrada_layout
        )

        layout.addWidget(
            self.tabela
        )

        layout.addWidget(
            self.lbl_total
        )

        self.setLayout(
            layout
        )

    # =========================================================
    # CONECTAR EVENTOS
    # =========================================================

    def conectar_eventos(self):

        self.botao_adicionar.clicked.connect(
            self.adicionar
        )

        self.botao_editar.clicked.connect(
            self.editar
        )

        self.botao_excluir.clicked.connect(
            self.excluir
        )

        self.quantidade.returnPressed.connect(
            self.adicionar
        )

    # =========================================================
    # ADICIONAR OMNICHANNEL
    # =========================================================

    def adicionar(self):

        texto = self.quantidade.text().strip()

        if not texto:
            return

        try:

            quantidade = int(texto)

        except ValueError:

            QMessageBox.warning(
                self,
                "Atenção",
                "Informe uma quantidade válida."
            )

            return

        if quantidade <= 0:

            QMessageBox.warning(
                self,
                "Atenção",
                "A quantidade deve ser maior que zero."
            )

            return

        # -----------------------------------------------------
        # DATA E HORA
        # -----------------------------------------------------

        agora = datetime.now()

        data = agora.strftime(
            "%d/%m/%Y"
        )

        hora = agora.strftime(
            "%H:%M"
        )

        # -----------------------------------------------------
        # SALVAR NO BANCO
        # -----------------------------------------------------

        salvar_omni(
            quantidade,
            data,
            hora
        )

        # -----------------------------------------------------
        # ATUALIZAR TABELA
        # -----------------------------------------------------

        self.carregar_do_banco()
        
        self.total_alterado.emit()

        self.quantidade.clear()
        self.quantidade.setFocus()

    # =========================================================
    # CARREGAR DO BANCO
    # =========================================================

    def carregar_do_banco(self):

        data = datetime.now().strftime(
            "%d/%m/%Y"
        )

        dados = buscar_omni_do_dia(
            data
        )

        self.tabela.setRowCount(0)

        for registro in dados:

            id_lancamento = registro[0]
            quantidade = registro[1]
            hora = registro[2]

            linha = self.tabela.rowCount()

            self.tabela.insertRow(
                linha
            )

            self.tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    str(id_lancamento)
                )
            )

            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    str(quantidade)
                )
            )

            self.tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    str(hora)
                )
            )

        self.atualizar_total()

    # =========================================================
    # EDITAR OMNICHANNEL
    # =========================================================

    def editar(self):

        linha = self.tabela.currentRow()

        if linha < 0:

            QMessageBox.warning(
                self,
                "Atenção",
                "Selecione um lançamento para editar."
            )

            return

        texto = self.quantidade.text().strip()

        if not texto:

            QMessageBox.warning(
                self,
                "Atenção",
                "Informe a nova quantidade."
            )

            return

        try:

            quantidade = int(texto)

        except ValueError:

            QMessageBox.warning(
                self,
                "Atenção",
                "Informe uma quantidade válida."
            )

            return

        if quantidade <= 0:

            QMessageBox.warning(
                self,
                "Atenção",
                "A quantidade deve ser maior que zero."
            )

            return

        # -----------------------------------------------------
        # PEGAR ID REAL DO BANCO
        # -----------------------------------------------------

        item_id = self.tabela.item(
            linha,
            0
        )

        if not item_id:
            return

        id_lancamento = int(
            item_id.text()
        )

        # -----------------------------------------------------
        # ATUALIZAR BANCO
        # -----------------------------------------------------

        atualizar_omni(
            id_lancamento,
            quantidade
        )

        # -----------------------------------------------------
        # RECARREGAR
        # -----------------------------------------------------

        self.carregar_do_banco()

        self.quantidade.clear()

        self.quantidade.setFocus()

    # =========================================================
    # EXCLUIR OMNICHANNEL
    # =========================================================

    def excluir(self):

        linha = self.tabela.currentRow()

        if linha < 0:

            QMessageBox.warning(
                self,
                "Atenção",
                "Selecione um lançamento para excluir."
            )

            return

        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            "Deseja realmente excluir este lançamento?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
        )

        if resposta != QMessageBox.StandardButton.Yes:
            return

        # -----------------------------------------------------
        # PEGAR ID REAL
        # -----------------------------------------------------

        item_id = self.tabela.item(
            linha,
            0
        )

        if not item_id:
            return

        id_lancamento = int(
            item_id.text()
        )

        # -----------------------------------------------------
        # EXCLUIR DO BANCO
        # -----------------------------------------------------

        excluir_omni(
            id_lancamento
        )

        # -----------------------------------------------------
        # RECARREGAR
        # -----------------------------------------------------

        self.carregar_do_banco()

    # =========================================================
    # ATUALIZAR TOTAL
    # =========================================================

    def atualizar_total(self):

        total = 0

        for linha in range(
            self.tabela.rowCount()
        ):

            item = self.tabela.item(
                linha,
                1
            )

            if item:

                try:

                    total += int(
                        item.text()
                    )

                except ValueError:

                    pass

        self.lbl_total.setText(
            f"Total OmniChannel: {total}"
        )

    # =========================================================
    # PEGAR TOTAL
    # =========================================================

    def obter_total(self):

        total = 0

        for linha in range(
            self.tabela.rowCount()
        ):

            item = self.tabela.item(
                linha,
                1
            )

            if item:

                try:

                    total += int(
                        item.text()
                    )

                except ValueError:

                    pass

        return total