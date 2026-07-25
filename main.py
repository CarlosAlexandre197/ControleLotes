import sys

from PySide6.QtWidgets import QApplication

from interface import Interface
from banco import criar_tabela

criar_tabela()


app = QApplication(sys.argv)

janela = Interface()
janela.show()

sys.exit(app.exec())