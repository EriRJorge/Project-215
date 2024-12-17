# Project 2151 - Notes App Lab
# eri r jorge & Zion 
# 12/02/2024 - created file and imported Pyside6.QtWidgets
# 12/02/2024 - created class CustomListWidget
# 12/02/2024 - created class ListNotesApp
# 12/03/2024 - added the save_file method
# 12/04/2024 - added TODOs
# 12/09/2024 - added the load_file method
# 12/09/2024 - added the TextEdit class
# 12/09/2024 - added the FolderTree class
# 12/10/2024 - added the NotesListWidget class
# 12/10/2024 - added the NotesApp class
# 12/11/2024 - added the setup_styling method to the NoteEditor class
# 12/12/2024 - added the SearchBar class
# 12/15/2024 - built the MVP
# 12/15/2024 - added the create_actions method
# 12/15/2024 - added the create_toolbar method
# 12/15/2024 - added the new_note method
# 12/15/2024 - added the save_note method
# 12/15/2024 - added the delete_note method
# 12/15/2024 - added the note_selected method
# 12/15/2024 - added the update_notes_list method
# 12/15/2024 - added the search_notes method
# 12/16/2024 - added all font methods to the NoteEditor class
# 12/16/2024 - added the closeEvent method



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
                              QLineEdit, QWidget, QHBoxLayout, 
                              QSplitter, QTextEdit, QColorDialog, QFontDialog, QMessageBox, QFileDialog, QComboBox,
                              QListWidget, QListWidgetItem, QMenu, QInputDialog, QVBoxLayout, QToolBar)
from PySide6.QtCore import Qt, QDateTime, Signal as pyqtSignal
from PySide6.QtGui import QFont, QColor, QKeyEvent, QTextCharFormat, QTextCursor, QFontDatabase, QAction
import sys
import os
import json
import shutil

class SearchBar(QLineEdit):
    searchRequested = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Search notes...")
        self.textChanged.connect(self.on_text_changed)
        self.setMinimumWidth(200)
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px;
                margin: 5px;
            }
        """)
    
    def on_text_changed(self, text):
        self.searchRequested.emit(text)

class NoteEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setup_styling()
<<<<<<< HEAD
        self.current_font = QFont()
        self.current_color = QColor(0, 0, 0)
        self.setup_styling()
=======
        self.current_file = None
>>>>>>> e813456420402d355d3864800b5a75a674241e35

    def setup_styling(self):
        self.setStyleSheet("""
            QTextEdit {
                background-color: #F9F1DC;
                border: none;
                padding: 20px;
                color: #333333;
            }
        """)

    def change_font(self, font_family):
        cursor = self.textCursor()
        if cursor.hasSelection():
            format = QTextCharFormat()
            format.setFontFamily(font_family)
            cursor.mergeCharFormat(format)
        else:
            self.setFontFamily(font_family)

    def change_font_size(self, size):
        cursor = self.textCursor()
        if cursor.hasSelection():
            format = QTextCharFormat()
            format.setFontPointSize(size)
            cursor.mergeCharFormat(format)
        else:
            self.setFontPointSize(size)

<<<<<<< HEAD
    def change_font(self): #TODO: Fix the font setting to change the font of the text
        font, ok = QFontDialog.getFont(self.current_font, self)
        if ok:
            self.current_font = font
            self.apply_text_styling()

    def change_font_color(self): #TODO: Fix the font setting to change the font of the text
        color = QColorDialog.getFont(self.current_font, self, "Choose Font Color")
        if color.isValid():
            self.current_color = color
            self.apply_text_styling()
        # color = QColorDialog.getColor(self.palette().color(self.foregroundRole()), self, "Choose Font Color")
        # if color.isValid():
        #     self.setStyleSheet(f"QTextEdit {{ color: {color.name()}; }}")

    def apply_text_styling(self):
        self.setFont(self.currentFont)
        palette = self.palette()
        palette.setColor(self.foregroundRole(), self.current_color)
        self.setPalette(palette)

        self.setStyleSheet(f"""
            QTextEdit {{
                           background-color: #F9F1DC;
                           border: none;
                           padding; 20px;
                           color: {self.current_color.name()};
            }}
    """)

    def change_background_color(self): #TODO: Fix the background color setting
        color = QColorDialog.getColor(self.palette().color(self.backgroundRole()), self, "Choose Background Color")
        if color.isValid():
            self.setStyleSheet(f"QTextEdit {{ background-color: {color.name()}; }})")

    def change_font_size(self, size): #TODO: Fix the font setting to change the font of the text
        font, ok =QFontDialog.getFont()
        if ok:
            self.setFont(font)

class FolderTree(QTreeWidget): #TODO: Fix the notes side to update when a new note is ad    ded
    def __init__(self):
        super().__init__()
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_menu)
        self.populate_tree()

    def populate_tree(self): #TODO: Fix the notes side to update when a new note is added
        self.root = QTreeWidgetItem(self, ["Folders"])
        self.addTopLevelItem(self.root)

    def open_menu(self, position):
        menu = QMenu()
        create_folder_action = menu.addAction("Create Folder")
        delete_folder_action = menu.addAction("Delete Folder")
        action = menu.exec_(self.viewport().mapToGlobal(position))
        
        if action == create_folder_action:
            self.create_folder()
        elif action == delete_folder_action:
            self.delete_folder()

    def create_folder(self):
        folder_name, ok = QInputDialog.getText(self, "Create Folder", "Folder Name:")
        if ok and folder_name:
            folder = QTreeWidgetItem(self.root, [folder_name])
            self.root.addChild(folder)

    def delete_folder(self):
        selected_item = self.currentItem()
        if selected_item and selected_item != self.root:
            index = self.indexFromItem(selected_item)
            self.takeTopLevelItem(index.row())

    def get_notes_for_folder(self, folder_name): # TODO: Logic to retrieve notes from the specified folder
        folder_path = os.path.join("notes", folder_name)
        if os.path.exists(folder_path):
            notes = os.listdir(folder_path)
            return [{"title": os.path.splitext(note)[0]} for note in notes]
=======
    def change_font_color(self, color):
        cursor = self.textCursor()
        if cursor.hasSelection():
            format = QTextCharFormat()
            format.setForeground(QColor(color))
            cursor.mergeCharFormat(format)
        else:
            self.setTextColor(QColor(color))

    def change_background_color(self, color):
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {color};
                border: none;
                padding: 20px;
                color: #333333;
            }}
        """)
>>>>>>> e813456420402d355d3864800b5a75a674241e35

class NotesListWidget(QListWidget):
    note_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.setStyleSheet("""
            QListWidget {
                background-color: #F5F5F5;
                border: none;
            }
            QListWidget::item {
                padding: 5px;
                margin: 2px;
                border-radius: 3px;
                color: #333333;
            }
            QListWidget::item:selected {
                background-color: #E0E0E0;
            }
        """)

    def show_context_menu(self, position):
        menu = QMenu()
        delete_action = menu.addAction("Delete Note")
        rename_action = menu.addAction("Rename Note")
        action = menu.exec_(self.mapToGlobal(position))

        if action == delete_action:
            self.delete_selected_note()
        elif action == rename_action:
            self.rename_selected_note()

    def delete_selected_note(self):
        current_item = self.currentItem()
        if current_item:
            reply = QMessageBox.question(self, 'Delete Note', 
                                       f'Are you sure you want to delete "{current_item.text()}"?',
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.takeItem(self.row(current_item))

    def rename_selected_note(self):
        current_item = self.currentItem()
        if current_item:
            new_name, ok = QInputDialog.getText(self, 'Rename Note', 
                                              'Enter new name:', 
                                              text=current_item.text())
            if ok and new_name:
                current_item.setText(new_name)

class NotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notes App")
        self.setGeometry(100, 100, 1200, 800)
        
        # set up the main window
        self.current_file = None
        self.setup_ui()
        self.create_actions()
        self.create_toolbar()
        
        # makes sure the notes folder exists
        if not os.path.exists("notes"):
            os.makedirs("notes")

    def setup_ui(self):
        # central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # main layout
        layout = QVBoxLayout(central_widget)
        
        # make search bar
        self.search_bar = SearchBar()
        self.search_bar.searchRequested.connect(self.search_notes)
        layout.addWidget(self.search_bar)
        
        # make splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # make and set up notes list
        self.notes_list = NotesListWidget()
        self.notes_list.itemClicked.connect(self.note_selected)
        splitter.addWidget(self.notes_list)
        
        # make and set up note editor
        self.note_editor = NoteEditor()
        splitter.addWidget(self.note_editor)
        
        layout.addWidget(splitter)

    def create_actions(self):
        # create actions
        self.new_action = QAction("New Note", self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.triggered.connect(self.new_note)

        self.save_action = QAction("Save Note", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_note)

        self.delete_action = QAction("Delete Note", self)
        self.delete_action.setShortcut("Delete")
        self.delete_action.triggered.connect(self.delete_note)

        self.color_action = QAction("Font Color", self)
        self.color_action.triggered.connect(self.change_color)

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # add actions to toolbar
        toolbar.addAction(self.new_action)
        toolbar.addSeparator()
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()
        toolbar.addAction(self.delete_action)
        toolbar.addSeparator()
        toolbar.addAction(self.color_action)
        
        # makes the font combo box
        self.font_combo = QComboBox()
        self.font_combo.addItems(QFontDatabase.families())
        self.font_combo.currentTextChanged.connect(
            lambda family: self.note_editor.change_font(family))
        toolbar.addWidget(self.font_combo)
        
        # adds the size combo box
        self.size_combo = QComboBox()
        sizes = [str(size) for size in [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 36, 48, 72]]
        self.size_combo.addItems(sizes)
        self.size_combo.setCurrentText("12")
        self.size_combo.currentTextChanged.connect(
            lambda size: self.note_editor.change_font_size(float(size)))
        toolbar.addWidget(self.size_combo)

    def new_note(self):
        self.note_editor.clear()
        self.current_file = None
        self.statusBar().showMessage("New note created")

    def save_note(self):
        if not self.note_editor.toPlainText().strip():
            QMessageBox.warning(self, "Error", "Cannot save empty note")
            return
            
        if not self.current_file:
            title, ok = QInputDialog.getText(self, "Save Note", "Enter note title:")
            if ok and title:
                self.current_file = os.path.join("notes", f"{title}.txt")
        
        if self.current_file:
            try:
                with open(self.current_file, 'w') as file:
                    file.write(self.note_editor.toPlainText())
                self.statusBar().showMessage(f"Saved to {self.current_file}")
                self.update_notes_list()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save note: {str(e)}")

    def delete_note(self):
        if not self.current_file:
            return
            
        reply = QMessageBox.question(self, "Delete Note",
                                   "Are you sure you want to delete this note?",
                                   QMessageBox.Yes | QMessageBox.No)
                                   
        if reply == QMessageBox.Yes:
            try:
                os.remove(self.current_file)
                self.new_note()
                self.update_notes_list()
                self.statusBar().showMessage("Note deleted")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete note: {str(e)}")

    def note_selected(self, item):
        file_path = os.path.join("notes", f"{item.text()}.txt")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.note_editor.setPlainText(file.read())
            self.current_file = file_path
            self.statusBar().showMessage(f"Loaded {file_path}")

    def update_notes_list(self):
        self.notes_list.clear()
        if os.path.exists("notes"):
            for filename in os.listdir("notes"):
                if filename.endswith(".txt"):
                    self.notes_list.addItem(filename[:-4])

    def search_notes(self, text):
        for i in range(self.notes_list.count()):
            item = self.notes_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def change_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.note_editor.setFont(font)

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.note_editor.change_font_color(color.name())

    def closeEvent(self, event):
        if self.note_editor.toPlainText().strip():
            reply = QMessageBox.question(self, "Save Changes",
                                       "Do you want to save your changes?",
                                       QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            
            if reply == QMessageBox.Yes:
                self.save_note()
                event.accept()
            elif reply == QMessageBox.No:
                event.accept()
            else:
                event.ignore()

def main():
    app = QApplication(sys.argv)
    window = NotesApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()