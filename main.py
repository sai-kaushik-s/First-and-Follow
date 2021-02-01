r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""
# Import the required libraries
import sys
from helperFunctions import setDarkMode
from GUIWindow import GUIWindow
from PyQt5.QtWidgets import *


# Main driver program of the client
if __name__ == '__main__':
    # Start a Qt application
    app = QApplication(sys.argv)
    # Set dark mode to the GUI
    setDarkMode(app)
    # Initialize the file dialog class
    ex = GUIWindow()
    # Show the file dialog window
    ex.show()
    # Exit the application, on click of close
    sys.exit(app.exec_())
