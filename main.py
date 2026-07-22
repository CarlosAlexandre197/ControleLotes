import sys

from PySide6.QtWidgets import QApplication

from interface import JanelaPrincipal
from banco import criar_tabela

criar_tabela()


app = QApplication(sys.argv)

janela = JanelaPrincipal()
janela.show()

sys.exit(app.exec())