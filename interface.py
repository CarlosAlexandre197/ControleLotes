from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QTableWidgetItem
)

from widgets.cadastro import CadastroWidget
from widgets.tabela import TabelaWidget
from widgets.finalizacao import FinalizacaoWidget
from widgets.indicadores import IndicadoresWidget
from widgets.omni import OmniWidget
from widgets.editar_lote import EditarLoteDialog
from widgets.pos_separacao import PosSeparacaoWidget

from banco import (
    salvar_lote,
    buscar_lotes_do_dia,
    atualizar_lote,
    excluir_lote_db,
    atualizar_separacao,
    atualizar_pos_separacao,
)


class Interface(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Controle de Lotes")
        self.resize(1500, 900)

        # Lote atualmente selecionado
        self.lote_selecionado = None

        self.criar_interface()
        self.conectar_eventos()

        self.carregar_lotes_do_dia()
        self.omni.carregar_do_banco()
        self.atualizar_indicadores()

    # =========================================================
    # CRIAR INTERFACE
    # =========================================================

    def criar_interface(self):

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
        
        linha_acoes = QHBoxLayout()

        self.botao_editar_lote = QPushButton("✏️ Editar Lote")
        self.botao_excluir_lote = QPushButton("🗑️ Excluir Lote")

        linha_acoes.addWidget(self.botao_editar_lote)
        linha_acoes.addWidget(self.botao_excluir_lote)

        layout_principal.addLayout(linha_acoes)

        # -----------------------------------------------------
        # PÓS-SEPARAÇÃO
        # -----------------------------------------------------

        self.pos_separacao = PosSeparacaoWidget()

        layout_principal.addWidget(
            self.pos_separacao
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

        # Cadastro
        self.cadastro.botao_salvar.clicked.connect(
            self.salvar
        )
        
        self.omni.total_alterado.connect(
            self.atualizar_indicadores
        )

        # Seleção de lote na tabela
        self.tabela.itemSelectionChanged.connect(
            self.selecionar_lote
        )

        # Finalizar separação
        self.finalizacao.botao_finalizar.clicked.connect(
            self.finalizar_separacao
        )

        # Salvar pós-separação
        self.pos_separacao.botao_salvar.clicked.connect(
            self.salvar_pos_separacao
        )

    # =========================================================
    # SALVAR LOTE
    # =========================================================

    def salvar(self):

        lote = self.cadastro.lote.text().strip()

        quantidade_texto = (
            self.cadastro.quantidade.text().strip()
        )

        cartoes_texto = (
            self.cadastro.cartoes.text().strip()
        )

        cancelados_texto = (
            self.cadastro.cancelados.text().strip()
        )

        # -----------------------------------------------------
        # VALIDAR LOTE
        # -----------------------------------------------------

        if not lote:

            QMessageBox.warning(
                self,
                "Atenção",
                "Informe o número do lote."
            )

            return

        # -----------------------------------------------------
        # CONVERTER VALORES
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
        # QUANTIDADE FINAL
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
        # SALVAR
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
        # ATUALIZAR
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

                item = QTableWidgetItem(
                    str(
                        valor
                        if valor is not None
                        else ""
                    )
                )

                self.tabela.setItem(
                    linha,
                    coluna,
                    item
                )

    # =========================================================
    # SELECIONAR LOTE
    # =========================================================

    def selecionar_lote(self):

        linha = self.tabela.currentRow()

        if linha < 0:

            self.lote_selecionado = None

            self.pos_separacao.limpar()

            return

        # =========================================================
        # PEGAR NÚMERO DO LOTE
        # =========================================================

        item_lote = self.tabela.item(
            linha,
            0
        )

        if not item_lote:
            return

        lote = item_lote.text()

        self.lote_selecionado = lote

        # =========================================================
        # BUSCAR DADOS COMPLETOS DO LOTE
        # =========================================================

        data = datetime.now().strftime(
            "%d/%m/%Y"
        )

        lotes = buscar_lotes_do_dia(
            data
        )

        dados_lote = None

        for dados in lotes:

            if str(dados[0]) == str(lote):

                dados_lote = dados

                break

        # =========================================================
        # SE NÃO ENCONTROU
        # =========================================================

        if dados_lote is None:

            self.pos_separacao.selecionar_lote(
                lote
            )

            return

        # =========================================================
        # DADOS DO PÓS-SEPARAÇÃO
        #
        # 9  = faturado
        # 10 = embarcado
        # 11 = pré-autorização
        # 12 = notas fiscais
        # =========================================================

        faturado = dados_lote[9]

        embarcado = dados_lote[10]

        pre_autorizacao = dados_lote[11]

        notas_impressas = dados_lote[12]

        # =========================================================
        # CARREGAR NO PAINEL
        # =========================================================

        self.pos_separacao.selecionar_lote(
            lote,
            faturado,
            embarcado,
            pre_autorizacao,
            notas_impressas
        )

    # =========================================================
    # FINALIZAR SEPARAÇÃO
    # =========================================================

    def finalizar_separacao(self):

        # -----------------------------------------------------
        # VERIFICAR LOTE SELECIONADO
        # -----------------------------------------------------

        linha = self.tabela.currentRow()

        if linha < 0:

            QMessageBox.warning(
                self,
                "Atenção",
                "Selecione um lote na tabela antes de concluir a separação."
            )

            return

        item_lote = self.tabela.item(
            linha,
            0
        )

        if not item_lote:

            return

        lote = item_lote.text()

        # -----------------------------------------------------
        # PEGAR DADOS
        # -----------------------------------------------------

        palete = (
            self.finalizacao.palete.text().strip()
        )

        montador = (
            self.finalizacao.montador.text().strip()
        )

        caixas_texto = (
            self.finalizacao.caixas.text().strip()
        )

        # -----------------------------------------------------
        # VALIDAR
        # -----------------------------------------------------

        if not palete:

            QMessageBox.warning(
                self,
                "Atenção",
                "Informe o palete."
            )

            return

        if not montador:

            QMessageBox.warning(
                self,
                "Atenção",
                "Informe o montador."
            )

            return

        try:

            caixas = int(
                caixas_texto
            )

        except ValueError:

            QMessageBox.warning(
                self,
                "Atenção",
                "A quantidade de caixas deve ser um número."
            )

            return

        if caixas < 0:

            QMessageBox.warning(
                self,
                "Atenção",
                "A quantidade de caixas não pode ser negativa."
            )

            return

        # -----------------------------------------------------
        # ATUALIZAR BANCO
        # -----------------------------------------------------

        atualizar_separacao(
            lote,
            palete,
            montador,
            caixas
        )

        # -----------------------------------------------------
        # ATUALIZAR TELA
        # -----------------------------------------------------

        self.carregar_lotes_do_dia()

        self.atualizar_indicadores()

        self.finalizacao.palete.clear()
        self.finalizacao.montador.clear()
        self.finalizacao.caixas.clear()

        QMessageBox.information(
            self,
            "Separação concluída",
            f"A separação do lote {lote} foi concluída."
        )

    # =========================================================
    # SALVAR PÓS-SEPARAÇÃO
    # =========================================================

    def salvar_pos_separacao(self):

        dados = (
            self.pos_separacao.obter_dados()
        )

        lote = dados["lote"]

        if not lote:

            QMessageBox.warning(
                self,
                "Atenção",
                "Selecione um lote na tabela."
            )

            return

        # -----------------------------------------------------
        # SALVAR NO BANCO
        # -----------------------------------------------------

        atualizar_pos_separacao(
            lote,
            dados["faturado"],
            dados["embarcado"],
            dados["pre_autorizacao"],
            dados["notas_impressas"]
        )

        QMessageBox.information(
            self,
            "Pós-separação",
            f"As informações do lote {lote} foram salvas."
        )

    # =========================================================
    # ATUALIZAR INDICADORES
    # =========================================================

    def atualizar_indicadores(self):

        total_lotes = (
            self.tabela.rowCount()
        )

        total_pedidos = 0
        total_caixas = 0

        pendentes = 0
        finalizados = 0

        for linha in range(
            self.tabela.rowCount()
        ):

            # -------------------------------------------------
            # QUANTIDADE FINAL
            # -------------------------------------------------

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

            # -------------------------------------------------
            # CAIXAS
            # -------------------------------------------------

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

            # -------------------------------------------------
            # STATUS
            # -------------------------------------------------

            item_status = self.tabela.item(
                linha,
                8
            )

            if item_status:

                status = (
                    item_status.text().lower()
                )

                if status == "pendente":

                    pendentes += 1

                elif status == "finalizado":

                    finalizados += 1

        total_omni = self.omni.obter_total()

        self.indicadores.atualizar(
            total_lotes,
            total_pedidos,
            total_caixas,
            pendentes,
            finalizados,
            total_omni
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