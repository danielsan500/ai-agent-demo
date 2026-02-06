import os
from google import types

def get_files_info(working_directory, directory="."):
    try:
        absolute_directory = os.path.abspath(working_directory) 
        target_dir = os.path.normpath(os.path.join(absolute_directory, directory))
        valid_target_dir = os.path.commonpath([absolute_directory, target_dir]) == absolute_directory
        files_info = []
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(os.path.join(absolute_directory,target_dir)):
            return f'Error: "{directory}" is not a directory'
        
        for item in os.listdir(target_dir) :
            checking_path = os.path.join(absolute_directory,target_dir, item)
            files_info.append(
                f"- {item}: file_size={os.path.getsize(checking_path)}, is_dir={os.path.isdir(checking_path)} \n"
            )
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"
