'''This is documentation of all the bugs and fixes in the listapp.py file

Fixed:
1.
Bug: The program does not have a delete function
Fix: Added a delete function to the program

2.
Bug: The program does not have a save function
Fix: Added a save function to the program

3.
Bug: The program does not have a load function
Fix: Added a load function to the program

4.
Bug: The program does not have a clear function
Fix: Added a clear function to the program

5.
Bug: The save function was not saving the notes in .txt files
Fix: had to change the os call to write the notes to a .txt file

6.
Bug: The load function was not loading the notes from the .txt files
Fix: had to change the os call to read the notes from a .txt file

7.
Bug: The app did not want to run with .standardFonts
Fix: had to change the font setting to QtFontDatabase
Error encountered:
# File "c:\Users\EriRJ\Documents\CPTR-456\Project-215\listapp.py", line 313, in setup_formatting_toolbar
    self.font_combo.addItems(QFontDialog.standardFonts())

8.
Bug: The app did not want to run with change_font_color
Fix: had to change the font color setting to QColorDialog
Error encountered:
File "c:\Users\EriRJ\Documents\CPTR-456\Project-215\listapp.py", line 331, in setup_formatting_toolbar
    font_color_btn.clicked.connect(self.change_font_color)

    
9.
Bug: The app did not want to run at all
Fix: had to make sure i was using up to date version of PySide6 information



TODO:
1.
Bug: Font setting does not change
Fix: TODO: Fix the font setting to change the font of the text

2.
Bug: notes side dose not update when added a new note
Fix: TODO: Fix the notes side to update when a new note is added

3.
Bug: files do not get saved when the program is closed
Fix: TODO: Fix the files to save when the program is closed

4.
Bug: The program does not have a search function
Fix: TODO: Add a search function to the program

5.
Bug: The app can not change background color
Fix: TODO: Add a function to change the background color of the app
Errors encountered: 
# TypeError: NoteEditor.change_background_color() takes 1 positional argument but 2 were given #

6. 😢😢😢😢😢😢😢😢😢😢😢
Bug: Aoo just dose not want to run anymore!!! I have no idea why
Fix: TODO: Fix the app to run again
Errors encountered:
Traceback (most recent call last):
  File "c:\Users\EriRJ\Documents\CPTR-456\Project-215\listapp.py", line 314, in <module>
    main()
  File "c:\Users\EriRJ\Documents\CPTR-456\Project-215\listapp.py", line 309, in main
    window = NotesApp()
             ^^^^^^^^^^
  File "c:\Users\EriRJ\Documents\CPTR-456\Project-215\listapp.py", line 159, in __init__
    self.setup_ui()
  File "c:\Users\EriRJ\Documents\CPTR-456\Project-215\listapp.py", line 176, in setup_ui
    self.search_bar.searchRequested.connect(self.search_notes) 
                                            ^^^^^^^^^^^^^^^^^
7.
Bug: when the font and font color are changed the change dose not stay and is applied through out all notes
Fix: TODO: Fix the font and font color to stay with the note that was changed
                                            
8.
Bug: when the app is closed the notes are not automatically reloaded after the app is opened again
Fix: TODO: Fix the notes to be automatically loaded when the app is opened again

9.
Bug: app dose not have a way to create bulleted list
Fix: TODO: Add a function to create a bulleted list

'''