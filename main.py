from PyQt5 import QtWidgets # import PyQt5 widgets
import sys
import time

from Model.Server import MQTTServer

def initInterface():
    # Create the application object
    app = QtWidgets.QApplication(sys.argv)
    # Create the form object
    first_window = QtWidgets.QWidget()
    # Set window size
    first_window.resize(400, 300)
    # Set the form title
    first_window.setWindowTitle("The first pyqt program")
    # Show form
    first_window.show()
    # Run the program
    sys.exit(app.exec())

def main() -> int:
    MQTTServer()

    initInterface()

    while (True):
        print("Say cheese")
        time.sleep(3)

    return 0

if __name__ == '__main__':
    sys.exit(main())