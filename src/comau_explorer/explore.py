import zipfile
from pathlib import Path

from src.comau_extract.extract_program import extract_program
from src.comau_model.program import ComauProgram


class ComauExplorer:
    def __init__(self, path: str) -> None:
        self.path: str = path

    def file_search(self, filename: str) -> str:
        for path in Path(self.path).rglob(filename):
            return str(path)
        return ""

    def file_unzip(self, zip_path: str, extract_to: str) -> None:
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)
                self.path = extract_to
        except zipfile.BadZipFile:
            print(f"Error: The file {zip_path} is not a zip file or it is corrupted.")
        except FileNotFoundError:
            print(f"Error: The file {zip_path} does not exist.")
        except Exception as e:
            print(f"An error occurred while unzipping the file: {e}")

    def file_read(self, file_path: str) -> str:
        # Read the file and return its contents
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            return f"File not found: {self.path}"
        except Exception as e:
            return f"An error occurred: {e}"

    def file_write(self, file_path: str, content: str) -> None:
        try:
            with open(file_path, "w") as file:
                file.write(content)
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")

    def get_program(self, program_name: str) -> ComauProgram:
        # Search for the program files
        cod_file_path: str = self.file_search(f"{program_name}.pdl")
        var_file_path: str = self.file_search(f"{program_name}.lsv")
        # If the program files are found
        cod_string: str = self.file_read(cod_file_path)
        if var_file_path:
            var_string: str = self.file_read(var_file_path)
            return extract_program(cod=cod_string, var=var_string)
        else:
            return extract_program(cod=cod_string)

    """    def file_translate(self, file_path) -> None:
        translate = subprocess.run(["Pdl2.exe", file_path], shell=True, check=True)"""
