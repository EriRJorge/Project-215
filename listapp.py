#Project 2151 - Notes App Lab
#eri r jorge & Zion 
#12/02/2024 - crated file and imported Pyside6.QtWidgets
#12/02/2024 - created class CustomListWidget
#12/02/2024 - created class ListNotesApp
#12/03/2024 - added the add_item method
#12/04/2024 - Added TODOs



"""MVP: The MVP for this project will be an app that:
1. Can save a .txt file
2. Load a .txt file
3. Has some resemblance to the wireframe
4. Is a .exe executable
5. User can type notes
6. User can format
7. User can delete notes"""


#imports
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QTreeWidget, QTreeWidgetItem,
                              QLineEdit, QVBoxLayout, QWidget, QHBoxLayout, QLabel, 
                              QSplitter, QTextEdit, QFrame)
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QIcon
import sys
import os
import json

class SearchBar(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Something")
        self.setStyleSheet("""
            QLineEdit {
                background-color: #F9F1DC;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px;
                margin: 10px;
                color: #333333;
            }
        """)

class NoteEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setup_styling()
        
    def setup_styling(self):
        self.setStyleSheet("""
            QTextEdit {
                background-color: #F9F1DC;
                border: none;
                padding: 20px;
                color: #333333;
            }
        """)
        font = QFont("Arial", 12)
        self.setFont(font)
        
    def sort_list(self): #TODO: change to sort by name of files
        self.list_widget.sortItems()

    def select_all_items(self): #TODO: change to select all files
        self.list_widget.selectAll()

    def deselect_all_items(self): #TODO: change to deselect all files
        self.list_widget.clearSelection()

    def save_files(self): #TODO: change to be able to save .txt files and name them
        items = []
        for i in range(self.list_widget.count()):
            items.append(self.list_widget.item(i).text())
        
        with open('list_items.json', 'w') as f:
            json.dump(items, f)

    def load_files(self): # TODO: change to be able to load .txt files
        try:
            if os.path.exists('list_items.json'):
                with open('list_items.json', 'r') as f:
                    items = json.load(f)
                    self.list_widget.addItems(items)
                    self.sort_list()
        except Exception as e:
            print(f"Error loading items: {e}")

class FolderTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setup_styling()
        self.setup_header()
        self.populate_tree()
        
    def setup_styling(self):
        self.setStyleSheet("""
            QTreeWidget {
                background-color: #F9F1DC;
                border: none;
                color: #333333;
            }
            QTreeWidget::item {
                padding: 5px;
                border-bottom: 1px solid transparent;
            }
            QTreeWidget::item:selected {
                background-color: #F9F1DC;
                color: #333333;
            }
        """)
        
    def setup_header(self):
        self.setHeaderHidden(True)
        
    def populate_tree(self):
        # All Notes section
        all_notes = QTreeWidgetItem(self)
        all_notes.setText(0, "All Notes")
        all_notes.setText(1, "2")
        
        # Trash section
        trash = QTreeWidgetItem(self)
        trash.setText(0, "Trash")
        trash.setText(1, "12")
        
        # Folders section
        folders_label = QTreeWidgetItem(self)
        folders_label.setText(0, "Folders")
        
        # Sum folder
        sum_folder = QTreeWidgetItem(folders_label)
        sum_folder.setText(0, "Sum")
        sum_folder.setExpanded(True)
        
        # Files in Sum folder
        sweet_txt = QTreeWidgetItem(sum_folder)
        sweet_txt.setText(0, "Sweet.txt")
        
        sour_txt = QTreeWidgetItem(sum_folder)
        sour_txt.setText(0, "Sour.txt")

class NotesListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Search bar
        self.search_bar = SearchBar()
        layout.addWidget(self.search_bar)
        
        # Notes list
        self.notes_frame = QFrame()
        self.notes_frame.setStyleSheet("""
            QFrame {
                background-color: #F9F1DC;
                border: none;
                color: #333333;
            }
        """)
        notes_layout = QVBoxLayout(self.notes_frame)
        
        # Add some sample notes
        date = QDateTime.currentDateTime().toString("MM/dd/yy h:mm")
        for name in ["Sweet.txt", "Sweet.txt"]:
            note_widget = QWidget()
            note_layout = QVBoxLayout(note_widget)
            note_layout.setContentsMargins(10, 5, 10, 5)
            
            title = QLabel(name)
            title.setStyleSheet("font-weight: bold;")
            date_label = QLabel(date)
            date_label.setStyleSheet("color: #333333; font-size: 10px;")
            
            note_layout.addWidget(title)
            note_layout.addWidget(date_label)
            notes_layout.addWidget(note_widget)
        
        layout.addWidget(self.notes_frame)

class NotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notes")
        self.setGeometry(100, 100, 1200, 800)
        self.setup_ui()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Folder tree
        self.folder_tree = FolderTree()
        self.folder_tree.setFixedWidth(200)
        
        # Notes list
        self.notes_list = NotesListWidget()
        self.notes_list.setFixedWidth(300)
        
        # Note editor
        self.note_editor = NoteEditor()
        
        # Add widgets to splitter
        splitter.addWidget(self.folder_tree)
        splitter.addWidget(self.notes_list)
        splitter.addWidget(self.note_editor)
        
        # Add splitter to layout
        layout.addWidget(splitter)
        
        # Set the sample content
        self.note_editor.setText("""Text Goes Here""")


    

def main():
    app = QApplication(sys.argv)
    window = NotesApp()
    window.show()
    sys.exit(app.exec())




#TODO: Ability to create folders
#TODO: Ability to save files in folders
#TODO: Ability to delete folders
#TODO: Ability to Change fonts
#TODO: Ability to change font size
#TODO: Ability to change font color
#TODO: Ability to change background color

if __name__ == "__main__":
    main()