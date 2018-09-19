import os

directory = '/Users/bneal/Desktop/annotation_tool/test_directory'

def ls_files(directory=directory):
    """Takes in a directory path and lists all files in the directory."""

    file_names = [file for file in os.listdir(directory)]
    return(file_names)

