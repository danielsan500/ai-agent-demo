import os
from config import MAX_CHARS
from google.genai import types
def get_file_content(working_directory, file_path):
    try:
        absolute_directory = os.path.abspath(working_directory) 
        target_dir = os.path.normpath(os.path.join(absolute_directory, file_path))
        valid_target_dir = os.path.commonpath([absolute_directory, target_dir]) == absolute_directory

        file_content = ""
        if not valid_target_dir:
            raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_dir):
            raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')

        with open(target_dir, "r") as f:
            file_content = f.read(MAX_CHARS)
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content       
        

    except Exception as e:
        return f"Error reading files: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists a specific file content within the allowed workspace",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to a specific the specific file which is meant to be read",
            ),
        },
        required=["file_path"]
    ),
)