# e-letters
import os
import shutil

# Path to the file that contains the search terms
SEARCH_FILE = "search//term.txt"
# Path to the file that contains the new names for the files
RENAME_FILE = "rename//file.txt"
# Source directory where the files are located
SOURCE_FILE = "source//directory"
# Target directory where the copied files will be stored
TARGET_DIRECTORY = "//target//directory"

# Function to read the search terms from a file
def read_search_terms(file_path):
    try:
        with open(file_path, 'r') as f:
            # Reads each line of the file and returns a list of terms, ignoring empty lines and comments
            return [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []

# Function to read the rename terms from a file
def read_rename_terms(file_path):
    try:
        with open(file_path, 'r') as f:
            # Reads each line of the file and returns a list of terms, ignoring empty lines and comments
            return [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []

# Function to find the latest file that contains the search term
def find_latest_file(root_dir, search_term):
    latest_file = None
    latest_time = 0
    # Walks through all directories and files from the root directory
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # Checks if the search term is in the file name
            if search_term in file:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path): 
                    file_time = os.path.getmtime(file_path)  # Gets the modification date of the file
                    # Updates the latest file if a newer one is found
                    if file_time > latest_time:
                        latest_file = file
                        latest_time = file_time
    return latest_file

# Function to copy a file to the target directory with a new name
def copy_file(source_file, target_dir, new_file_name):
    try:
        destination_path = os.path.join(target_dir, new_file_name)
        # Checks if the destination file already exists
        if os.path.exists(destination_path):
            print(f"File '{new_file_name}' already exists in '{target_dir}'.")
            return False
        shutil.copy(source_file, destination_path)  # Copies the file
        return True
    except Exception as e:
        print(f"Error copying file '{source_file}' to '{destination_path}': {e}")
        return False

# Main function to manage the e-letters process
def e_letters(folder_name):
    search_terms = read_search_terms(SEARCH_FILE)  # Reads the search terms
    rename_terms = read_rename_terms(RENAME_FILE)  # Reads the rename terms

    # Checks if the number of search terms and rename terms is equal
    if len(search_terms) != len(rename_terms):
        print("Number of search terms and rename terms is different.")
        return

    # Checks if the search terms or rename terms are empty
    if not search_terms or not rename_terms:
        print("No search or rename terms found.")
        return

    target_folder = os.path.join(TARGET_DIRECTORY, folder_name)  # Creates the target folder path
    os.makedirs(target_folder, exist_ok=True)  # Creates the folder if it doesn't exist

    # Iterates over the search and rename terms
    for search_term, rename_term in zip(search_terms, rename_terms):
        latest_file = find_latest_file(SOURCE_FILE, search_term)  # Finds the latest file that contains the search term
        if latest_file:
            new_file_name = f"{rename_term}.pdf"  # Defines the new file name
            # Copies the found file to the target directory with the new name
            if copy_file(os.path.join(SOURCE_FILE, latest_file), target_folder, new_file_name):
                print(f"'{search_term}' was found and copied to the folder '{folder_name}'.")
        else:
            print(f"No file found for the search term '{search_term}'.")

# Main function that starts the process
def main():
    folder_name = input("Enter the folder name: ").strip()  # Prompts the user for the folder name
    # Checks if the folder name is valid
    if not folder_name:
        print("Invalid folder name.")
        return
    if any(char in folder_name for char in r'\/:*?"<>|'):
        print("Folder name contains invalid characters.")
        return
    e_letters(folder_name)  # Calls the main function to process the e-letters

# Checks if the script is being executed directly
if __name__ == "__main__":
    main()  # Starts the program      
