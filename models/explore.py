import os
import zipfile


class Explore:
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

    def cod_file(self, program_name) -> str:
        cod_file = self.file_search(f"{program_name}.pdl")
        if cod_file:
            return self.file_read(cod_file)
        else:
            return f"File {program_name}.pdl not found"

    def var_file(self, program_name) -> str:
        var_file = self.file_search(f"{program_name}.lsv")
        if var_file:
            return self.file_read(var_file)
        else:
            return f"File {program_name}.lsv not found"
