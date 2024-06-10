# folder_manager/folder_manager.py
import os
import shutil
import argparse

class Folder:
    def __init__(self, path, verbose=True):
        self.path = os.path.abspath(path)
        self.verbose = verbose

    def _print(self, message):
        if self.verbose:
            print(message)

    def create_folder(self):
        try:
            os.makedirs(self.path, exist_ok=True)
            self._print(f"Folder created at: {self.path}")
            return True
        except Exception as e:
            self._print(f"An error occurred: {e}")
            return False

    def list_files(self):
        try:
            files = os.listdir(self.path)
            self._print(f"Files in {self.path}: {files}")
            return files
        except Exception as e:
            self._print(f"An error occurred: {e}")
            return []

    def count_files(self):
        try:
            files = os.listdir(self.path)
            file_count = len(files)
            self._print(f"Number of files in {self.path}: {file_count}")
            return file_count
        except Exception as e:
            self._print(f"An error occurred: {e}")
            return 0

    def create_file(self, file_name, content=""):
        try:
            with open(os.path.join(self.path, file_name), 'w') as file:
                file.write(content)
            self._print(f"File '{file_name}' created with content: {content}")
            return True
        except Exception as e:
            self._print(f"An error occurred: {e}")
            return False

    def delete_file(self, file_name):
        try:
            os.remove(os.path.join(self.path, file_name))
            self._print(f"File '{file_name}' deleted")
            return True
        except Exception as e:
            self._print(f"An error occurred: {e}")
            return False

    def delete_folder(self):
        try:
            shutil.rmtree(self.path)
            self._print(f"Folder '{self.path}' and all its contents deleted")
            return True
        except Exception as e:
            self._print(f"An error occurred: {e}")
            return False

    def move_file(self, src, dest):
        try:
            shutil.move(src, dest)
            self._print(f"File moved from {src} to {dest}")
            return True
        except Exception as e:
            self._print(f"An error occurred: {e}")
            return False

    def copy_file(self, src, dest):
        try:
            shutil.copy2(src, dest)
            self._print(f"File copied from {src} to {dest}")
            return True
        except Exception as e:
            self._print(f"An error occurred: {e}")
            return False

    def folder_exists(self):
        exists = os.path.exists(self.path)
        if exists:
            self._print(f"Folder '{self.path}' exists")
        else:
            self._print(f"Folder '{self.path}' does not exist")
        return exists

def main():
    parser = argparse.ArgumentParser(description="Folder Manager CLI")
    parser.add_argument("action", choices=[
        "create_folder", "list_files", "count_files", "create_file",
        "delete_file", "delete_folder", "move_file", "copy_file", "folder_exists"
    ], help="Action to perform")
    parser.add_argument("path", help="Path to the folder")
    parser.add_argument("--file_name", help="File name for create_file, delete_file, move_file, copy_file actions")
    parser.add_argument("--content", help="Content for create_file action")
    parser.add_argument("--dest", help="Destination for move_file, copy_file actions")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    folder = Folder(args.path, verbose=args.verbose)
    print(f"Action: {args.action}, Path: {args.path}, Verbose: {args.verbose}")  # Debug print

    if args.action == "create_folder":
        folder.create_folder()
    elif args.action == "list_files":
        folder.list_files()
    elif args.action == "count_files":
        folder.count_files()
    elif args.action == "create_file":
        if args.file_name and args.content is not None:
            folder.create_file(args.file_name, args.content)
        else:
            print("file_name and content are required for create_file action")
    elif args.action == "delete_file":
        if args.file_name:
            folder.delete_file(args.file_name)
        else:
            print("file_name is required for delete_file action")
    elif args.action == "delete_folder":
        folder.delete_folder()
    elif args.action == "move_file":
        if args.file_name and args.dest:
            folder.move_file(args.file_name, args.dest)
        else:
            print("file_name and dest are required for move_file action")
    elif args.action == "copy_file":
        if args.file_name and args.dest:
            folder.copy_file(args.file_name, args.dest)
        else:
            print("file_name and dest are required for copy_file action")
    elif args.action == "folder_exists":
        folder.folder_exists()

if __name__ == "__main__":
    main()
