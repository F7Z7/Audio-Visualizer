import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
