r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""
# Import the required libraries
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from Grammar import Grammar


# Center Align Delegate for the table
class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter


# Class for the GUI Window
class GUIWindow(QWidget):
    # Init function for the class
    def __init__(self, parent=None, *argv, **kwargs):
        super(GUIWindow, self).__init__(parent, *argv, **kwargs)
        # Set the window title
        self.setWindowTitle("First and Follow of a Grammar")
        self.hint = QLabel("Add the start symbol production in the first.\nUse -> for transition and ~ for epsilon "
                           "and | alternate move")
        # Creating a group box
        self.formGroupBox = QGroupBox("Grammar")
        # Creating a text edit for the productions
        self.productions = QTextEdit()
        # Creating a line edit for the start symbol
        self.start = QLineEdit()
        # Create a button for running the functions
        self.button = QPushButton("Compute")
        # On click property of the button
        self.button.clicked.connect(self.getInfo)
        # Table widget for the outputs
        self.tableWidget = QTableWidget()
        # Stretch table to fit
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Initialize a center delegate
        delegate = AlignDelegate(self.tableWidget)
        # Set the delegate
        self.tableWidget.setItemDelegate(delegate)
        # Set read only for the entries
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Line text for terminals
        self.terminals = QLineEdit()
        # Set read only
        self.terminals.setReadOnly(True)
        # Line text for non terminals
        self.nonTerminals = QLineEdit()
        # Set read only
        self.nonTerminals.setReadOnly(True)
        # calling the method that create the form
        self.createForm()
        # creating a vertical layout
        mainLayout = QVBoxLayout()
        # Adding the hint
        mainLayout.addWidget(self.hint)
        # adding form group box to the layout
        mainLayout.addWidget(self.formGroupBox)
        # setting lay out
        self.setLayout(mainLayout)

    # Create form method
    def createForm(self):
        # Creating a form layout
        layout = QFormLayout()
        # Adding rows
        # Input of the productions and start symbol
        layout.addRow(QLabel("Productions"), self.productions)
        layout.addRow(QLabel("Start Symbol"), self.start)
        # Button for compute
        layout.addRow(self.button)
        # Output of terminals, non terminals and the first and follow of the grammar
        layout.addRow(QLabel("Non Terminals"), self.nonTerminals)
        layout.addRow(QLabel("Terminals"), self.terminals)
        layout.addRow(QLabel("Output"), self.tableWidget)
        # Setting layout
        self.formGroupBox.setLayout(layout)

    # Get information from the aforementioned form
    def getInfo(self):
        # Make a list of the productions
        productionsList = [y for y in (x.strip() for x in self.productions.toPlainText().splitlines()) if y]
        productionsDict = {}
        # Convert the productions to a dictionary
        # Key is the LSH
        # Value is the list of transitions
        for _ in productionsList:
            x = _.replace(" ", "").split("->")
            y = x[1].split("|")
            productionsDict[x[0]] = y
        # Get the start symbol
        startSymbol = self.start.text()
        NT = []
        T = []
        first = {}
        follow = {}
        # Append the non terminals to the list
        # Create a set for first and follow of each non terminal
        for i in productionsDict:
            NT.append(i)
            first[i] = set()
            follow[i] = set()
        # Append the terminals to the list
        for i in productionsDict:
            for j in productionsDict[i]:
                for k in j:
                    if k not in NT:
                        T.append(k)
                        first[k] = set(k)
                        follow[k] = set(k)

        # Remove duplicates from non terminals and terminals
        NT = list(set(NT))
        T = list(set(T))
        # Initialize the Grammar class
        grammar = Grammar(productionsDict, startSymbol, NT, T, first, follow)
        # Set the terminals and non terminals in the text fields
        self.terminals.setText(str(grammar.T))
        self.nonTerminals.setText(str(grammar.NT))
        # Get the first of the non terminals
        grammar.getFirst()
        # Get the follow of the non terminals
        grammar.getFollow()
        # Create the table of first and follow
        self.creatingTables(grammar)

    # A function to set the QTableWidget
    def creatingTables(self, grammar):
        # Set the row and column count
        self.tableWidget.setRowCount(len(grammar.NT) + 1)
        self.tableWidget.setColumnCount(3)
        # Set the headers of the columns
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Non-Terminals"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("First"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("Follow"))
        # Set each column with the first and follow data
        for i in range(len(grammar.NT)):
            follow = 'N/A' if len(grammar.follow[grammar.NT[i]]) == 0 else str(grammar.follow[grammar.NT[i]])
            self.tableWidget.setItem(i + 1, 0, QTableWidgetItem(grammar.NT[i]))
            self.tableWidget.setItem(i + 1, 1, QTableWidgetItem(str(grammar.first[grammar.NT[i]])))
            self.tableWidget.setItem(i + 1, 2, QTableWidgetItem(follow))
