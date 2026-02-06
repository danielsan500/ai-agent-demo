import os

def write_file(working_directory, file_path, content):
    try:
        absolute_directory = os.path.abspath(working_directory) 
        target_dir = os.path.normpath(os.path.join(absolute_directory, file_path))
        valid_target_dir = os.path.commonpath([absolute_directory, target_dir]) == absolute_directory

        if not valid_target_dir:
            raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if os.path.isdir(target_dir):
            raise Exception(f'Error: Cannot write to "{file_path}" as it is a directory')

        os.makedirs(absolute_directory, exist_ok=True)

        with open(target_dir, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error writting files: {e}"