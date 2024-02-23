from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QGridLayout, QWidget, QSplitter, QFrame, QLabel, QLineEdit, QVBoxLayout, QScrollArea, QFormLayout, QLayout, QMessageBox,
    QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt, QTimer
import sys
from dataclasses import dataclass

@dataclass
class Card:
    front: str
    back: str
    guessed: bool = False

@dataclass
class CardSet:
    name: str
    cards: list[Card]

class MainWindow(QMainWindow):
    BUTTON_STYLES = """
        QPushButton {
            background-color: lightgray;
        }
        QPushButton:pressed {
            background-color: darkgray;
        }
    """

    def create_create_button(self) -> QPushButton:
        button = QPushButton("Create set")
        button.setFixedSize(100, 50)
        button.setStyleSheet(self.BUTTON_STYLES)
        button.pressed.connect(self.show_create_set_form)
        return button
    
    def create_show_button(self) -> QPushButton:
        button = QPushButton("All sets")
        button.setFixedSize(100, 50)
        button.setStyleSheet(self.BUTTON_STYLES)
        button.pressed.connect(self.show_all_sets)
        return button
    
    def create_close_button(self) -> QPushButton:
        button = QPushButton("Close")
        button.setFixedSize(100, 50)
        button.setStyleSheet(self.BUTTON_STYLES)
        button.pressed.connect(self.delayed_close)
        return button

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Welcome!")
        self.setGeometry(100, 100, 800, 600)

        self.card_sets: list[CardSet] = []

        create_set_button = self.create_create_button()
        all_sets_button = self.create_show_button()
        close_button = self.create_close_button()

        left_frame = QFrame()
        right_frame = QFrame()
        left_frame.setStyleSheet("background-color: gray;")
        left_layout = QGridLayout()
        left_layout.addWidget(create_set_button, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        left_layout.addWidget(all_sets_button, 1, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        left_layout.addWidget(close_button, 2, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        left_frame.setLayout(left_layout)

        self.left_frame = left_frame
        self.right_frame = right_frame

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.left_frame)
        self.splitter.addWidget(self.right_frame)
        self.splitter.setSizes([200, 600])

        self.setCentralWidget(self.splitter)
        self.show_create_set_form()
        self.show()

    def delayed_close(self):
        QTimer.singleShot(200, self.close)

    def show_create_set_form(self):
        self.right_frame = QFrame()  # Create a new QFrame

        layout = QVBoxLayout()
        self.set_form = QFormLayout()
        layout.addLayout(self.set_form)

        add_card_button = QPushButton("+")
        add_card_button.pressed.connect(self.add_card_form)
        layout.addWidget(add_card_button)

        save_set_button = QPushButton("Save set")
        save_set_button.pressed.connect(self.save_set)
        layout.addWidget(save_set_button)

        self.right_frame.setLayout(layout)
        self.add_card_form()

        self.refresh_right_frame()
                
    def show_all_sets(self):
        self.right_frame = QFrame()  # Create a new QFrame
        layout = QVBoxLayout()
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Set", "Cards"])
        for set_index, card_set in enumerate(self.card_sets, start=1):
            cards_text = "\n".join(f"Card {card_index + 1}: {card.front} - {card.back}" 
                                for card_index, card in enumerate(card_set.cards))
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(f"Set {set_index}"))
            table.setItem(row, 1, QTableWidgetItem(cards_text))
        layout.addWidget(table)
        self.right_frame.setLayout(layout)
        self.refresh_right_frame()

    def refresh_right_frame(self):
        self.splitter.replaceWidget(1, self.right_frame)  # Replace the old right frame with the new one


    def add_card_form(self):
        self.set_form.addRow(QLineEdit(), QLineEdit())

    def save_set(self):
        cards = []
        for i in range(0, self.set_form.rowCount()):
            back_item = self.set_form.itemAt(i, QFormLayout.ItemRole.FieldRole).widget()
            front_item = self.set_form.itemAt(i, QFormLayout.ItemRole.LabelRole).widget()
            if front_item is not None and back_item is not None:
                front = front_item.text()
                back = back_item.text()
                # Check if both the front and back fields are not empty
                if front and back:
                    cards.append(Card(front, back))
        self.card_sets.append(CardSet("Set " + str(len(self.card_sets) + 1), cards))
        # Show a prompt after saving the set
        QMessageBox.information(self, "Set created", f"Set with {len(cards)} cards is created")
        # Clear the form
        self.show_create_set_form()

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            # Create a new layout to replace the old one
            parent = layout.parentWidget()
            if parent is not None:
                new_layout = QVBoxLayout()
                parent.setLayout(new_layout)

app = QApplication(sys.argv)
w = MainWindow()
app.exec()