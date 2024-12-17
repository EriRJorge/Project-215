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
# 12/17/2024 - added the make_bullet_points method to the NoteEditor class
# 12/17/2024 - added the KeyPressEvent method to the NoteEditor class




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
        self.current_file = None

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

    def change_font_size(self, size):
        cursor = self.textCursor()
        if cursor.hasSelection():
            format = QTextCharFormat()
            format.setFontPointSize(size)
            cursor.mergeCharFormat(format)

    def change_font_color(self, color):
        cursor = self.textCursor()
        if cursor.hasSelection():
            format = QTextCharFormat()
            format.setForeground(QColor(color))
            cursor.mergeCharFormat(format)

    def change_background_color(self, color):
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {color};
                border: none;
                padding: 20px;
                color: #333333;
            }}
        """)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            cursor = self.textCursor()
            current_block = cursor.block().text()

            if current_block.strip().startswith('• '):
                # If the current line is just a bullet point, remove it
                if current_block.strip() == '• ':
                    cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
                    cursor.removeSelectedText()
                    self.setTextCursor(cursor)
                else:
                    # Insert a new line and a bullet point
                    super().keyPressEvent(event)
                    cursor = self.textCursor()
                    cursor.insertText("• ")
                    self.setTextCursor(cursor)
                return

        super().keyPressEvent(event)
    
    def make_bullet_points(self):
        cursor = self.textCursor()
        cursor.insertText('• ')
        self.setTextCursor(cursor)


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
        
        # Initialize attributes
        self.current_file = None
        self.setup_ui()
        self.create_actions()
        self.create_toolbar()
        
        # makes sure the notes folder exists
        if not os.path.exists("notes"):
            os.makedirs("notes")

        # update notes list
        self.update_notes_list()

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
        # file actions
        self.new_action = QAction("New", self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.triggered.connect(self.new_note)

        self.save_action = QAction("Save", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_note)

        self.delete_action = QAction("Delete", self)
        self.delete_action.setShortcut("Delete")
        self.delete_action.triggered.connect(self.delete_note)

        self.color_action = QAction("Color", self)
        self.color_action.triggered.connect(self.change_color)

        self.bullet_action = QAction("Bullet", self)
        self.bullet_action.triggered.connect(self.make_bullet_points)

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # adds action buttons to toolbar
        toolbar.addAction(self.new_action)
        toolbar.addSeparator()
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()
        toolbar.addAction(self.delete_action)
        toolbar.addSeparator()
        toolbar.addAction(self.color_action)
        toolbar.addSeparator()
        toolbar.addAction(self.bullet_action)
        
        # adds font combo
        self.font_combo = QComboBox()
        self.font_combo.addItems(QFontDatabase.families())
        self.font_combo.currentTextChanged.connect(
            lambda family: self.note_editor.change_font(family))
        toolbar.addWidget(self.font_combo)
        
        # adds size combo
        self.size_combo = QComboBox()
        sizes = [str(size) for size in [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 36, 48, 72]]
        self.size_combo.addItems(sizes)
        self.size_combo.setCurrentText("12")
        self.size_combo.currentTextChanged.connect(
            lambda size: self.note_editor.change_font_size(float(size)))
        toolbar.addWidget(self.size_combo)


    def make_bullet_points(self):
        self.note_editor.make_bullet_points()

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
            cursor = self.note_editor.textCursor()
        if cursor.hasSelection():
            format = QTextCharFormat()
            format.setFont(font)
            cursor.mergeCharFormat(format)

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