import os, subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        absolute_directory = os.path.abspath(working_directory) 
        target_dir = os.path.normpath(os.path.join(absolute_directory, file_path))
        valid_target_dir = os.path.commonpath([absolute_directory, target_dir]) == absolute_directory

        if not valid_target_dir:
            raise Exception(f'Error: Cannot execute "{file_path}" as it is outside')
        if not os.path.isfile(target_dir):
            raise Exception(f'Error: "{file_path}" does not exist')
        
        if not file_path[-3:] == ".py":
            raise Exception(f'"{file_path}" is not a Python file')
        
        command = ["python", target_dir]
        if args is not None:
            command.extend(args)


        resultado_proceso = subprocess.run(command, text=True, capture_output=True, timeout=30)
        respuesta = ""
        if resultado_proceso.returncode != 0:
            respuesta+= f"Process exited with code {resultado_proceso.returncode}"
        if resultado_proceso.stdout is None and resultado_proceso.stderr is None:
            respuesta+= f"No output produced"
            return respuesta
        if resultado_proceso.stdout is not None:
            respuesta+= f"STDOUT: {resultado_proceso.stdout}"
        if resultado_proceso.stderr is not None:
            respuesta+= f"STDERR: {resultado_proceso.stderr}"
        return respuesta
    except Exception as e:
        return f"{e}"

# no se como hacer el nested ARGS
schema_run_python_info = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specific python file. It takes a path to the file that have to be executed and optional arguments to execute it",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to the Python file to execute",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments to pass to the python file. Default None",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Single argument to pass to the Python file",
                ),
            ),
        },
        required=["file_path", "args"]
    ),
)