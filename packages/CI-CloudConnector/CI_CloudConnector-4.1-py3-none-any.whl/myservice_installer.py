import os
import shutil
import subprocess
import time


def copy_files(files, destination_dir):
    """
    Copies a list of files to the specified destination directory.

    Parameters:
    files (list): List of file paths to copy.
    destination_dir (str): The destination directory.
    """
    for source_file in files:
        try:
            shutil.copy(source_file, destination_dir)
            print(f"File '{source_file}' copied successfully to '{destination_dir}'.")
        except FileNotFoundError as fnf_error:
            print(f"File not found: {fnf_error}")
        except Exception as e:
            print(f"An error occurred while copying '{source_file}': {e}")


def move_files(python_dir):
    """
    Handles copying necessary files to the specified Python directory.

    Parameters:
    python_dir (str): The directory where Python executable is located.
    """

    source_file = os.path.join(python_dir, "Lib", "site-packages", "win32", "pythonservice.exe")
    copy_files([source_file], python_dir)

    source_file = os.path.join(python_dir, "misc.py")
    destination_file = os.path.join(python_dir, "Lib", "site-packages", "cpppo")
    copy_files([source_file], destination_file)


def get_python_executable_directory():
    """
    Finds the directory path of the Python executable using the 'where python' command on Windows.

    Returns:
    str: The directory path of the Python executable if found, otherwise raises an exception.
    """
    try:
        # Run the 'where python' command
        result = subprocess.run(['where', 'python'], capture_output=True, text=True, check=True)

        # The output contains the path(s) to the Python executable(s)
        python_paths = result.stdout.splitlines()

        if python_paths:
            # Get the first path found and return its directory
            python_executable_path = python_paths[0]
            python_executable_dir = os.path.dirname(python_executable_path)

            # Ensure the directory is the correct Python installation directory
            # Check if the path ends with 'python.exe'
            if python_executable_path.endswith('python.exe'):
                # Return the directory containing the executable
                return python_executable_dir
            else:
                raise RuntimeError("Unexpected output from 'where python' command.")
        else:
            raise FileNotFoundError("No Python executable found using 'where python'.")

    except subprocess.CalledProcessError as cpe:
        raise RuntimeError(f"Subprocess error: {cpe.stderr}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")


def main():
    try:
        python_exe_dir = get_python_executable_directory()
        move_files(python_exe_dir)
        time.sleep(10)
    except (FileNotFoundError, ValueError) as fnf_error:
        print(f"Configuration error: {fnf_error}")
    except subprocess.CalledProcessError as cpe:
        print(f"Subprocess error: {cpe.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == '__main__':
    main()