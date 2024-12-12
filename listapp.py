#list notes app
#eri r jorge & Zion 
#10/23/2024 - crated file and imported Pyside6.QtWidgets
"""MVP: The MVP for this project will be an app that:
1. Can save a .txt file
2. Load a .txt file
3. Has some resemblance to the wireframe
4. Is a .exe executable
5. User can type notes
6. User can format
7. User can delete notes"""

from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                              QListWidget, QLineEdit, QVBoxLayout, 
                              QWidget, QHBoxLayout, QMessageBox, QListWidgetItem)
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
import json
import os

class CustomListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.last_clicked_item = None

    def mousePressEvent(self, event: QMouseEvent):
        item = self.itemAt(event.pos())
        if item and event.modifiers() == Qt.ShiftModifier:
            # Toggle the selection state of the clicked item
            item.setSelected(not item.isSelected())
            self.last_clicked_item = item
        else:
            # Default handling for other cases
            super().mousePressEvent(event)
            if item:
                self.last_clicked_item = item

class ListNotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("List Notes App")
        self.setGeometry(100, 100, 400, 500)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create input field and buttons
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter new item...")
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_item)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.add_button)
        
        # Create custom list widget
        self.list_widget = CustomListWidget()
        
        # Create button layout
        button_layout = QHBoxLayout()
        
        # Create remove button for multiple items
        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self.remove_items)
        
        # Create select all button
        self.select_all_button = QPushButton("Select All")
        self.select_all_button.clicked.connect(self.select_all_items)
        
        # Create deselect all button
        self.deselect_all_button = QPushButton("Deselect All")
        self.deselect_all_button.clicked.connect(self.deselect_all_items)
        
        # Add buttons to button layout
        button_layout.addWidget(self.select_all_button)
        button_layout.addWidget(self.deselect_all_button)
        button_layout.addWidget(self.remove_button)
        
        # Add widgets to layout
        layout.addLayout(input_layout)
        layout.addWidget(self.list_widget)
        layout.addLayout(button_layout)
        
        # Load saved items
        self.load_items()
        
        # Connect enter key to add item
        self.input_field.returnPressed.connect(self.add_item)

    def add_item(self):
        text = self.input_field.text().strip()
        if text:
            self.list_widget.addItem(text)
            self.input_field.clear()
            self.save_items()
            self.sort_list()

    def remove_items(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Information", "Please select items to remove")
            return
            
        confirmation = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to remove {len(selected_items)} item(s)?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirmation == QMessageBox.Yes:
            for item in selected_items:
                self.list_widget.takeItem(self.list_widget.row(item))
            self.save_items()
            self.sort_list()

    def sort_list(self):
        self.list_widget.sortItems()

    def select_all_items(self):
        self.list_widget.selectAll()

    def deselect_all_items(self):
        self.list_widget.clearSelection()

    def save_items(self):
        items = []
        for i in range(self.list_widget.count()):
            items.append(self.list_widget.item(i).text())
        
        with open('list_items.json', 'w') as f:
            json.dump(items, f)

    def load_items(self):
        try:
            if os.path.exists('list_items.json'):
                with open('list_items.json', 'r') as f:
                    items = json.load(f)
                    self.list_widget.addItems(items)
                    self.sort_list()
        except Exception as e:
            print(f"Error loading items: {e}")

    def closeEvent(self, event):
        self.save_items()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication([])
    window = ListNotesApp()
    window.show()
    app.exec()