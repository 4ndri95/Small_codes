import os
import shutil
import concurrent.futures

# Define the target directory for the found files
TARGET_DIRECTORY = "target//directory"

# Define the source directories for the search
SOURCE_DIRECTORIES = {
    "directory_1": "//source//directory_1",
    "directory_2": "//source//directory_2",
    "directory_3": "//source//directory_3",
    "directory_4": "//source//directory_4",
    "toi": {  # TOI directory with subdirectories by year
        "2019": "//source//directory//2019",
        "2020": "//source//directory//2020",
        "2021": "//source//directory//2021",
        "2022": "//source//directory//2022",
        "2023": "//source//directory//2023",
        "2024": "//source//directory//2024",
    }
}

# Function to clear the console screen
def clear_console():
    # Uses the "cls" command on Windows or "clear" on other systems
    os.system("cls" if os.name == "nt" else "clear")

# Function to process the search terms in a source directory
def process_search_terms(search_terms, source_directory, target_directory):
    # Iterate over the search terms
    for search_term in search_terms:
        search_term = search_term.strip()  # Remove whitespace
        term_folder = os.path.join(target_directory, search_term)  # Create a directory for the search term
        os.makedirs(term_folder, exist_ok=True)  # Create the directory if it doesn't exist

        # Iterate over the files in the source directory
        for root, dirs, files in os.walk(source_directory):
            for file in files:
                if search_term in file:  # Check if the search term is in the file name
                    file_path = os.path.join(root, file)  # Full path of the file
                    if source_directory == SOURCE_DIRECTORIES["directory_3"]:
                        new_file_name = f"Schedule_{file}"  # Rename the file to include "Schedule_"
                    else:
                        new_file_name = file  # Keep the original file name
                    new_file_path = os.path.join(term_folder, new_file_name)  # Full path of the renamed file
                    shutil.copy2(file_path, new_file_path)  # Copy the file to the target directory
                    search_file_message(file, source_directory)  # Display message of found file
                    break  # Exit the loop to avoid finding the same file again

# Function to search for terms in a specific TOI directory
def toi_search(year, search_terms, target_directory):
    source_directory = SOURCE_DIRECTORIES["toi"][year]  # Select the TOI directory for the specified year
    process_search_terms(search_terms, source_directory, target_directory)  # Call the function to process search terms

# Function to display message of found file
def search_file_message(file, source_directory):
    if source_directory == SOURCE_DIRECTORIES["directory_3"]:
        print(f"'Schedule_{file} was found'")  # Display a custom message for scheduling
    else:
        print(f"'{file}' was found.")  # Display standard message for other directories

# Main function of the program
def main():
    while True:
        search_terms = input("Enter the search UCs, separated by commas: ").split(',')  # Ask the user to enter search terms
        clear_console()  # Clear the console screen
        target_directory = TARGET_DIRECTORY  # Define the target directory
        if search_terms[0].strip() == "":  # Check if the user entered anything
            print("You did not enter any search UC. Please try again.")
            print("")
        else:
            # Create a thread executor to process the searches in parallel
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                futures.append(executor.submit(process_search_terms, search_terms, SOURCE_DIRECTORIES["directory_1"], target_directory))
                futures.append(executor.submit(process_search_terms, search_terms, SOURCE_DIRECTORIES["directory_2"], target_directory))
                futures.append(executor.submit(process_search_terms, search_terms, SOURCE_DIRECTORIES["directory_3"], target_directory))
                futures.append(executor.submit(process_search_terms, search_terms, SOURCE_DIRECTORIES["directory_4"], target_directory))
                for year in SOURCE_DIRECTORIES["toi"]:
                    futures.append(executor.submit(toi_search, year, search_terms, target_directory))
                concurrent.futures.wait(futures)  # Wait for all threads to finish

if __name__ == "__main__":
    main()  # Call the main function of the program
