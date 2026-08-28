from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)

from widgets.cadastro import CadastroWidget
from widgets.tabela import TabelaWidget
from widgets.finalizacao import FinalizacaoWidget
from widgets.indicadores import IndicadoresWidget
from widgets.omni import OmniWidget

from banco import (
    salvar_lote,
    buscar_lotes_do_dia,
)


class Interface(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Controle de Lotes")
        self.resize(1500, 900)

        self.criar_interface()
        self.conectar_eventos()

        self.carregar_lotes_do_dia()
        self.atualizar_indicadores()

    # =========================================================
    # CRIAR INTERFACE
    # =========================================================

    def criar_interface(self):

        # Widget central
        central = QWidget()
        self.setCentralWidget(central)

        layout_principal = QVBoxLayout()
        central.setLayout(layout_principal)

        # -----------------------------------------------------
        # PARTE SUPERIOR
        # -----------------------------------------------------

        linha_superior = QHBoxLayout()

        self.cadastro = CadastroWidget()
        self.finalizacao = FinalizacaoWidget()

        linha_superior.addWidget(
            self.cadastro,
            1
        )

        linha_superior.addWidget(
            self.finalizacao,
            1
        )

        layout_principal.addLayout(
            linha_superior
        )

        # -----------------------------------------------------
        # TABELA
        # -----------------------------------------------------

        self.tabela = TabelaWidget()

        layout_principal.addWidget(
            self.tabela,
            3
        )

        # -----------------------------------------------------
        # INDICADORES
        # -----------------------------------------------------

        self.indicadores = IndicadoresWidget()

        layout_principal.addWidget(
            self.indicadores
        )

        # -----------------------------------------------------
        # OMNICHANNEL
        # -----------------------------------------------------

        self.omni = OmniWidget()

        layout_principal.addWidget(
            self.omni,
            2
        )

    # =========================================================
    # CONECTAR EVENTOS
    # =========================================================

    def conectar_eventos(self):

        self.cadastro.botao_salvar.clicked.connect(
            self.salvar
        )

    # =========================================================
    # SALVAR LOTE
    # =========================================================

    def salvar(self):

        lote = self.cadastro.lote.text().strip()
        quantidade_texto = self.cadastro.quantidade.text().strip()
        cartoes_texto = self.cadastro.cartoes.text().strip()
        cancelados_texto = self.cadastro.cancelados.text().strip()

        # -----------------------------------------------------
        # VALIDAÇÃO DO LOTE
        # -----------------------------------------------------

        if not lote:

            QMessageBox.warning(
                self,
                "Atenção",
                "Informe o número do lote."
            )

            return

        # -----------------------------------------------------
        # CONVERTER QUANTIDADE
        # -----------------------------------------------------

        try:

            quantidade = int(
                quantidade_texto
            )

            cartoes = int(
                cartoes_texto or 0
            )

            cancelados = int(
                cancelados_texto or 0
            )

        except ValueError:

            QMessageBox.warning(
                self,
                "Atenção",
                "Quantidade, cartões e cancelados devem ser números."
            )

            return

        # -----------------------------------------------------
        # VALIDAÇÕES
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # CALCULAR QUANTIDADE FINAL
        # -----------------------------------------------------

        quantidade_final = (
            quantidade
            - cartoes
            - cancelados
        )

        if quantidade_final < 0:

            QMessageBox.warning(
                self,
                "Erro",
                "Quantidade final não pode ser negativa."
            )

            return

        # -----------------------------------------------------
        # DATA
        # -----------------------------------------------------

        data = datetime.now().strftime(
            "%d/%m/%Y"
        )

        # -----------------------------------------------------
        # SALVAR NO BANCO
        # -----------------------------------------------------

        salvar_lote(
            lote,
            quantidade,
            cartoes,
            cancelados,
            quantidade_final,
            data
        )

        # -----------------------------------------------------
        # ATUALIZAR INTERFACE
        # -----------------------------------------------------

        self.carregar_lotes_do_dia()

        self.atualizar_indicadores()

        self.limpar_cadastro()

        QMessageBox.information(
            self,
            "Lote cadastrado",
            f"Lote {lote} cadastrado com sucesso."
        )

    # =========================================================
    # CARREGAR LOTES DO DIA
    # =========================================================

    def carregar_lotes_do_dia(self):

        data = datetime.now().strftime(
            "%d/%m/%Y"
        )

        lotes = buscar_lotes_do_dia(
            data
        )

        self.tabela.setRowCount(0)

        for lote in lotes:

            linha = self.tabela.rowCount()

            self.tabela.insertRow(
                linha
            )

            for coluna, valor in enumerate(lote):

                self.tabela.setItem(
                    linha,
                    coluna,
                    __import__(
                        "PyQt6.QtWidgets",
                        fromlist=["QTableWidgetItem"]
                    ).QTableWidgetItem(
                        str(
                            valor if valor is not None else ""
                        )
                    )

    # =========================================================
    # ATUALIZAR INDICADORES
    # =========================================================

    def atualizar_indicadores(self):

        total_lotes = self.tabela.rowCount()

        total_pedidos = 0
        total_caixas = 0

        pendentes = 0
        finalizados = 0

        for linha in range(
            self.tabela.rowCount()
        ):

            # Quantidade Final
            item_final = self.tabela.item(
                linha,
                4
            )

            if item_final:

                try:
                    total_pedidos += int(
                        item_final.text()
                    )

                except ValueError:
                    pass

            # Caixas
            item_caixas = self.tabela.item(
                linha,
                7
            )

            if item_caixas:

                try:
                    total_caixas += int(
                        item_caixas.text()
                    )

                except ValueError:
                    pass

            # Status
            item_status = self.tabela.item(
                linha,
                8
            )

            if item_status:

                status = item_status.text().lower()

                if status == "pendente":
                    pendentes += 1

                elif status == "finalizado":
                    finalizados += 1

        self.indicadores.atualizar(
            total_lotes,
            total_pedidos,
            total_caixas,
            pendentes,
            finalizados
        )

    # =========================================================
    # LIMPAR CADASTRO
    # =========================================================

    def limpar_cadastro(self):

        self.cadastro.lote.clear()
        self.cadastro.quantidade.clear()
        self.cadastro.cartoes.clear()
        self.cadastro.cancelados.clear()

        self.cadastro.lote.setFocus()


# =============================================================
# INICIAR PROGRAMA
# =============================================================

if __name__ == "__main__":

    app = QApplication([])

    janela = Interface()

    janela.show()

    app.exec()