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
                              QSplitter, QTextEdit, QFrame, QColorDialog, QFontDialog, QMessageBox, QFileDialog, QComboBox,
                              QListWidget, QListWidgetItem, QMenu, QInputDialog)
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QFont, QColor
import sys
import os
import json
import shutil

class SearchBar(QLineEdit):# TODO: Add a search function to the program
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Search")
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
    
    def search(self):
        pass

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

    def save_file(self, file_path):
        try:
            with open(file_path, "w") as file:
                file.write(self.toPlainText())
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save file: {e}")

    def load_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                self.setText(file.read())
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load file: {e}")

    def change_font(self): #TODO: Fix the font setting to change the font of the text
        font, ok = QFontDialog.getFont()
        if ok:
            self.setFont(font)

    def change_font_color(self): #TODO: Fix the font setting to change the font of the text
        color = QColorDialog.getColor(self.palette().color(self.foregroundRole()), self, "Choose Font Color")
        if color.isValid():
            self.setStyleSheet(f"QTextEdit {{ color: {color.name()}; }}")

    def change_background_color(self): #TODO: Fix the background color setting
        color = QColorDialog.getColor(self.palette().color(self.backgroundRole()), self, "Choose Background Color")
        if color.isValid():
            self.setStyleSheet(f"QTextEdit {{ background-color: {color.name()}; }})")

    def change_font_size(self, size): #TODO: Fix the font setting to change the font of the text
        font = self.font()
        font.setPointSize(size)
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

class NotesListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_menu)
        self.notes = []

    def update_notes(self, notes):
        self.clear()
        self.notes = notes
        for note in self.notes:
            item = QListWidgetItem(note['title'])
            self.addItem(item)

    def open_menu(self, position):
        menu = QMenu()
        edit_action = menu.addAction("Edit Note")
        delete_action = menu.addAction("Delete Note")
        action = menu.exec_(self.viewport().mapToGlobal(position))
        
        if action == edit_action:
            self.edit_note()
        elif action == delete_action:
            self.delete_note()

    def edit_note(self): #TODO: add logic to edit the note
        selected_item = self.currentItem()
        if selected_item:
            note_title = selected_item.text()

            pass

    def delete_note(self):
        selected_item = self.notes_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Delete Note", "No note selected.")
            return

        note_title = selected_item.text()
        folder = self.folder_tree.currentItem().text(0) if self.folder_tree.currentItem() else "Default"
        note_path = os.path.join("notes", folder, f"{note_title}.txt")

        reply = QMessageBox.question(
            self, "Delete Note", f"Are you sure you want to delete the note '{note_title}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                os.remove(note_path)
                self.notes_list.takeItem(self.notes_list.row(selected_item))
                QMessageBox.information(self, "Delete Note", "Note deleted successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete note: {e}")


class NotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notes")
        self.setGeometry(100, 100, 1200, 800)
        self.setup_ui()


    def setup_ui(self): #TODO: Fix the font setting to change the font of the text & clean up the UX
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
        self.folder_tree.itemClicked.connect(self.folder_selected)

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

        # Add actions
        self.create_actions()

    def create_actions(self): #TODO: Creates a real file in directory
        toolbar = self.addToolBar("Actions")

        # Save note
        save_action = QPushButton("Save")
        save_action.clicked.connect(self.save_note)
        toolbar.addWidget(save_action)

        # Load note
        load_action = QPushButton("Load")
        load_action.clicked.connect(self.load_note)
        toolbar.addWidget(load_action)

        # Add folder
        add_folder_action = QPushButton(" + Folder")
        add_folder_action.clicked.connect(self.add_folder)
        toolbar.addWidget(add_folder_action)

        # Delete folder
        delete_folder_action = QPushButton(" - Folder")
        delete_folder_action.clicked.connect(self.delete_folder)
        toolbar.addWidget(delete_folder_action)

        # Change font
        font_action = QPushButton("Change Font")
        font_action.clicked.connect(self.change_font)
        toolbar.addWidget(font_action)

        # Change font color
        font_color_action = QPushButton("Font Color")
        font_color_action.clicked.connect(self.change_font_color)
        toolbar.addWidget(font_color_action)

        # Change background color
        bg_color_action = QPushButton("Background Color")
        bg_color_action.clicked.connect(self.change_background_color)
        toolbar.addWidget(bg_color_action)


    def save_note(self):
        note_title = self.note_editor.toPlainText().split('\n')[0]
        folder = self.folder_tree.currentItem().text(0) if self.folder_tree.currentItem() else "Default"
        file_path = os.path.join("notes", folder, f"{note_title}.txt")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(self.note_editor.toPlainText())
        QMessageBox.information(self, "Save Note", "Note saved successfully.")

    def load_note(self):
        folder = self.folder_tree.currentItem().text(0) if self.folder_tree.currentItem() else "Default"
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Note", os.path.join("notes", folder), "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.note_editor.setPlainText(content)

    def add_folder(self):
        self.folder_tree.create_folder()

    def delete_folder(self):
        folder_to_del = self.folder_tree.currentItem()
        prompt = QMessageBox.question(self, "Delete Folder", f"Are you sure you want to delete the folder'{folder_to_del.text(0)} '?", QMessageBox.Yes | QMessageBox.No)

        if prompt == QMessageBox.Yes:
            folder_del_name = folder_to_del.text(0)
            folder_del_path = os.path.join("notes", folder_del_name)

            shutil.rmtree(folder_del_path)

            parent = folder_to_del.parent()
            if parent:
                parent.removeChild(folder_to_del)

            QMessageBox.information(self, "Delete Folder", "Folder Deleted")
        else:
            QMessageBox.information(self, "Delete Folder", "Folder not Deleted")
        
        self.folder_tree.delete_folder()

    def delete_note(self):
        note_to_del = self.currentItem()
        if not note_to_del:
            return
    
        note_title = note_to_del.text()

        reply = QMessageBox.question(self, "Delete Note", f"Are you sure you want to delete the note '{note_title}'?", QMessageBox.Yes | QMessageBox.No)
    
        if reply == QMessageBox.Yes:
            current_folder = self.parent().folder_tree.currentItem().text(0) if self.parent().folder_tree.currentItem() else "Default"

            file_path = os.path.join("notes", current_folder, f"{note_title}.txt")
        
            try:

                os.remove(file_path)

                self.takeItem(self.row(note_to_del))
            
                QMessageBox.information(self, "Delete Note", "Note deleted successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Delete Note", f"Failed to delete note: {str(e)}")

    def folder_selected(self, item, column):
        folder_name = item.text(0)
        notes = self.folder_tree.get_notes_for_folder(folder_name)
        self.notes_list.update_notes(notes)

    def change_font(self): #TODO: Fix the font setting to change the font of the text
        font, ok = QFontDialog.getFont()
        if ok:
            self.note_editor.change_font(font.family())

    def change_font_size(self): #TODO: Fix the font setting to change the font of the text
        size, ok = QInputDialog.getInt(self, "Font Size", "Enter font size:", min=8, max=48)
        if ok:
            self.note_editor.change_font_size(size)

    def change_font_color(self): #TODO: Fix the font setting to change the font of the text
        color = QColorDialog.getColor()
        if color.isValid():
            self.note_editor.change_font_color(color.name())

    def change_background_color(self): #TODO: Fix the background color setting
        color = QColorDialog.getColor()
        if color.isValid():
            self.note_editor.change_background_color(color.name())

def main():
    app = QApplication(sys.argv)
    window = NotesApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()