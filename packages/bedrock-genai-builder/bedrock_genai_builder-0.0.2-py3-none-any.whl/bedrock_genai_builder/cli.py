# cli.py
import click
import os
import subprocess
from pathlib import Path
from bedrock_genai_builder.code_content import code_structure_list

allowed_files = {
    "LAMBDA": ["lambda_function.py", "prompt_store.yaml"],
    "NON_LAMBDA": ["bedrock_app.py", "prompt_store.yaml"],
}


def create_lambda_handler(app_type, code_path):
    for code_data in code_structure_list:
        if code_data["file_name"] in allowed_files[app_type]:
            file_path = os.path.join(code_path, code_data["file_name"])

            with open(file_path, "w") as file:
                file.write(code_data["code"])


@click.command()
@click.option(
    "--app_type",
    required=True,
    type=str,
    help="Provide app type - LAMBDA or NON_LAMBDA",
)
@click.argument("root_dir")
def create_gen_ai_project_structure(app_type, root_dir):
    base_path = Path(root_dir).resolve()
    lib_dir = os.path.join(base_path, "bedrock_util")

    # Create build directory
    os.makedirs(lib_dir)

    # install boto3
    subprocess.check_call(["pip", "install", "boto3", "-t", base_path])

    subprocess.check_call(
        ["pip", "install", "bedrock-genai-util", "pyyaml", "-t", lib_dir]
    )

    create_lambda_handler(app_type, base_path)


if __name__ == "__main__":
    create_gen_ai_project_structure()
