# utils/file_operations.py
import os
import pandas as pd

# Function to check if a file is a CSV file
def is_csv(file):
    """
    Checks if the uploaded file is a CSV file based on the file extension.
    
    Arguments:
    - file: The file object uploaded by the user (Flask's file storage object)
    
    Returns:
    - bool: True if the file has a '.csv' extension, otherwise False
    """
    return file.filename.endswith('.csv')

# Function to save the uploaded file to a specific directory
def save_uploaded_file(file, save_path='./data/'):
    """
    Saves the uploaded file to the specified directory.
    
    Arguments:
    - file: The file object to be saved
    - save_path: The directory where the file will be saved (default: './data/')
    
    Returns:
    - str: The full path where the file was saved
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)  # Create the directory if it doesn't exist
    
    file_path = os.path.join(save_path, file.filename)
    file.save(file_path)  # Save the file to the specified path
    return file_path

# Function to load a CSV file into a pandas DataFrame
def load_csv(file_path):
    """
    Loads a CSV file into a pandas DataFrame.
    
    Arguments:
    - file_path: The path of the CSV file to be loaded
    
    Returns:
    - pd.DataFrame: The loaded CSV data as a pandas DataFrame
    """
    if os.path.exists(file_path):
        try:
            data = pd.read_csv(file_path)
            return data
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return None
    else:
        print(f"File not found: {file_path}")
        return None

# Function to check if a file exists in the specified directory
def file_exists(file_name, directory='./data/'):
    """
    Checks if a file exists in the specified directory.
    
    Arguments:
    - file_name: The name of the file to check for
    - directory: The directory to search for the file (default: './data/')
    
    Returns:
    - bool: True if the file exists, False otherwise
    """
    return os.path.exists(os.path.join(directory, file_name))

# Function to delete a file from the server (e.g., for cleaning up or replacing files)
def delete_file(file_name, directory='./data/'):
    """
    Deletes a file from the specified directory.
    
    Arguments:
    - file_name: The name of the file to be deleted
    - directory: The directory where the file is stored (default: './data/')
    
    Returns:
    - bool: True if the file was successfully deleted, False if the file doesn't exist
    """
    file_path = os.path.join(directory, file_name)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    else:
        print(f"File not found: {file_path}")
        return False
