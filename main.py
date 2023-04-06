from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QSizeGrip,
    QWidget,
    QFrame,
)
from PyQt5.QtCore import (
    QLine,
    QPoint,
    QSize,

)

from src.modelling import SupermarketModel
from src.ui_v2 import Ui_SupermarketModelUI

if __name__ == "__main__":
    app = QApplication([])
    window = QMainWindow()
    window.setFixedSize(1200, 800)
    ui = Ui_SupermarketModelUI()
    ui.setupUi(window)
    window.show()
    app.exec()
