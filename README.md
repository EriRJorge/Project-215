#Set up#
1. run pip install PySide6 (if using VsCode)
2. run .exe file in the exe file folder otherwise



#Instructions for Lab#
Lab Assignment: Building a Notes App
Replacing Lab B (Tic-Tac-Toe)

Overview
This lab enhances the previous Shopping List GUI warm-up into a full-featured Notes application similar to Apple Notes but for PC. 
Students will build on top of their existing knowledge of GUI programming to create a notes app.

Learning Objectives
1. Implement a complex graphical user interface using PySide6
2. Work with file systems and directory manipulation in Python
3. Create persistent storage solutions for application data
4. Apply software design principles in a real-world application
5. Practice unit testing with Qt Test framework
6. Package a Python application for distribution

Prerequisites
* Completion of Shopping List GUI warm-up
* Basic understanding of Python and PySide6
* Familiarity with version control (Git)

Required Tools
1. Python 
2. VS Code or preferred IDE
3. PySide6 module
4. Git/GitHub account
5. Code Together extension (for pair programming)

Helper Functions
The following helper functions are provided in the starter code:


def create_note_file(title, content):
    """Creates a new note file with given title and content"""
    pass

def load_note(file_path):
    """Loads and returns contents of a note file"""
    pass

def save_note(note_obj):
    """Saves note object to file system"""
    pass

def search_notes(query):
    """Searches through note titles and content"""
    pass


Implementation Steps

Step 1: Basic Note Management
Implement the core functionality for creating and managing notes:
* Create new notes
* Edit existing notes
* Delete notes
* Save notes to files
* Load notes from files

Step 2: File Organization
Implement file system operations:
* Create folders
* Move notes between folders
* Directory navigation
* File search functionality

Step 3: User Interface
Develop the complete UI according to the wireframe:
* Main window layout
* Note list sidebar
* Text editing area
* Formatting toolbar
* Search bar

Deliverables
1. Complete source code via GitHub repository
2. Executable (.exe) version of the application
4. Documentation including:
   * Bugs encountered
   * Code Documentation
   * Read Me

Grading Criteria
* Functionality (40%)
* Code quality and organization (20%)
* User interface design (15%)
* Ux (15%)
* Documentation (10%)

Resources
* PySide6 Documentation
* Qt Test Framework Guide
* Python File System Operations Guide
* Auto-py-to-exe Documentation

Optional Extensions
* Cloud synchronization
* Rich text formatting
* Note sharing capabilities
* Dark mode support

Submission Guidelines
1. Push final code to GitHub repository
2. Submit executable file
3. Provide access to repository to course staff
4. Include all documentation in repository

 Time to complete
* Lab sessions: 1 weeks
