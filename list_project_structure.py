import os
import json
from pathlib import Path

def get_directory_structure(startpath, exclude_dirs=None, exclude_files=None):
    if exclude_dirs is None:
        exclude_dirs = {'.git', '__pycache__', 'node_modules', '.next'}
    if exclude_files is None:
        exclude_files = {'.gitignore', '.env', '.DS_Store'}
    
    directory_structure = {}
    
    for root, dirs, files in os.walk(startpath):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        # Get the current level in the directory structure
        level = os.path.relpath(root, startpath).split(os.sep)
        current_dict = directory_structure
        
        # Navigate to the current level in our dictionary
        for part in level:
            if part == '.':
                continue
            current_dict = current_dict.setdefault(part, {})
        
        # Add files at this level
        files = [f for f in files if f not in exclude_files]
        if files:
            current_dict['files'] = sorted(files)
    
    return directory_structure

def print_structure(structure, indent='', is_last=True, parent_prefix=''):
    items = list(structure.items())
    
    for index, (name, content) in enumerate(items):
        if name == 'files':
            for file_index, file in enumerate(content):
                is_last_file = file_index == len(content) - 1
                prefix = '└── ' if is_last_file and index == len(items) - 1 else '├── '
                print(f'{parent_prefix}{prefix}{file}')
        else:
            is_last_item = index == len(items) - 1 and 'files' not in structure
            prefix = '└── ' if is_last_item else '├── '
            print(f'{parent_prefix}{prefix}{name}/')
            
            new_parent_prefix = parent_prefix + ('    ' if is_last_item else '│   ')
            print_structure(content, indent + '  ', is_last_item, new_parent_prefix)

def main():
    # Get the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    print(f"Project Structure for: {os.path.basename(project_root)}")
    print("=" * 50)
    
    # Get the directory structure
    structure = get_directory_structure(project_root)
    
    # Print the tree structure
    print_structure(structure)
    
    # Save the structure to a JSON file for reference
    json_path = os.path.join(project_root, 'project_structure.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 50)
    print(f"Structure has also been saved to: {json_path}")

if __name__ == '__main__':
    main()