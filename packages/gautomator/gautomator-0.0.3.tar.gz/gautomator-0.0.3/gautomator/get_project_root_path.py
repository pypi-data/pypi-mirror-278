import os

@staticmethod
def find_project_root(marker_files=('setup.py', 'requirements.txt', '.git')):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    while current_dir != os.path.abspath(os.sep):
        for marker in marker_files:
            if os.path.exists(os.path.join(current_dir, marker)):
                return current_dir
        current_dir = os.path.dirname(current_dir)
    return None
