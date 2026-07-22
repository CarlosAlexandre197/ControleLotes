import sys

from PySide6.QtWidgets import QApplication

from interface import JanelaPrincipal


app = QApplication(sys.argv)

janela = JanelaPrincipal()
janela.show()

sys.exit(app.exec())