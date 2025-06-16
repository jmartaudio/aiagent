from google.genai import types

from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def check_verbose_true(function_call_part, verbose):
    if verbose is True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")


def call_function(function_call_part, verbose=False):
    if function_call_part.name == "get_files_info":
        check_verbose_true(function_call_part, verbose)
        respose = get_files_info(
            **{
                "working_directory": "./calculator/",
                "file_path": f"{function_call_part.args}",
            }
        )
    elif function_call_part.name == "get_file_content":
        check_verbose_true(function_call_part, verbose)
        respose = get_file_content(
            **{
                "working_directory": "./calculator/",
                "file_path": f"{function_call_part.args}",
            }
        )
    elif function_call_part.name == "run_python_file":
        check_verbose_true(function_call_part, verbose)
        respose = run_python_file(
            **{
                "working_directory": "./calculator/",
                "file_path": f"{function_call_part.args}",
            }
        )
    elif function_call_part.name == "write_file":
        check_verbose_true(function_call_part, verbose)
        respose = write_file(
            **{
                "working_directory": "./calculator/",
                "file_path": f"{function_call_part.args}",
                "content": f"{content}",
            }
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": f"{respose}"},
            )
        ],
    )
