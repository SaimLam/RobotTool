import os
import zipfile

from src.models.comau_program import ComauProgram


class ComauExplorer:
    def __init__(self, path) -> None:
        self.path = path

    def file_search(self, filename) -> str:
        # Search for a file in the directory
        for root, dirs, files in os.walk(self.path):
            if filename in files:
                # Return the path of the file
                return os.path.join(root, filename)
        return ""

    def file_unzip(self, zip_path, extract_to) -> None:
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

    def file_read(self, file_path) -> str:
        # Read the file and return its contents
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            return f"File not found: {self.path}"
        except Exception as e:
            return f"An error occurred: {e}"

    def file_write(self, file_path, content) -> None:
        try:
            with open(file_path, "w") as file:
                file.write(content)
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")

    """    def file_translate(self, file_path) -> None:
        translate = subprocess.run(["Pdl2.exe", file_path], shell=True, check=True)"""

    def get_program(self, program_name: str) -> ComauProgram | str:
        # Search for the program files
        cod_file_path = self.file_search(f"{program_name}.pdl")
        var_file_path = ""
        if cod_file_path:
            var_file_path = self.file_search(f"{program_name}.lsv")
        # If the program files are found
        if cod_file_path:
            cod_string = self.file_read(cod_file_path)
            if var_file_path:
                var_string = self.file_read(var_file_path)
                return ComauProgram(cod_string=cod_string, var_string=var_string)
            else:
                return ComauProgram(cod_string=cod_string)
        else:
            return f"File {program_name}.pdl not found"
