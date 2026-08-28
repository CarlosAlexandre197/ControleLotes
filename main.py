import sys

from PySide6.QtWidgets import QApplication

from interface import Interface
from banco import criar_tabela

criar_tabela()


app = QApplication(sys.argv)

app.setStyleSheet("""
    QWidget {
        background-color: #121212;
        color: white;
        font-size: 14px;
    }

    QMainWindow {
        background-color: #121212;
    }

    QLabel {
        color: white;
    }

    QLineEdit {
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #555555;
        border-radius: 5px;
        padding: 6px;
    }

    QPushButton {
        background-color: #2d2d2d;
        color: white;
        border: 1px solid #555555;
        border-radius: 5px;
        padding: 7px 12px;
    }

    QPushButton:hover {
        background-color: #404040;
    }

    QTableWidget {
        background-color: #1e1e1e;
        color: white;
        gridline-color: #444444;
        border: 1px solid #555555;
        selection-background-color: #3d5a80;
        selection-color: white;
    }

    QHeaderView::section {
        background-color: #2d2d2d;
        color: white;
        padding: 6px;
        border: 1px solid #444444;
    }

    QCheckBox {
        color: white;
    }

    QGroupBox {
        color: white;
        border: 1px solid #555555;
        border-radius: 6px;
        margin-top: 10px;
        padding-top: 10px;
    }

    QComboBox {
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #555555;
        border-radius: 5px;
        padding: 5px;
    }
""")

janela = Interface()

janela.show()

sys.exit(app.exec())