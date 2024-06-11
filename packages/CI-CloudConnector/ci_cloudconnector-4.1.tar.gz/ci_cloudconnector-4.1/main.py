import logic
import sys
import subprocess
import shutil
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Timer
from datetime import datetime

UPGRADE_COUNTER = 0
SERVER_VERSION = ""
REPEATING_TIMER = None
SERVICE_STOP = 0


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False



def update_and_run(script_path, package_name, package_version):
    try:

        logic.ci_print(f'Attempting to update package {package_name} to version {package_version}')

        current_script_dir = os.path.dirname(os.path.abspath(__file__))

        if package_version == '':
            # Upgrade the package
            command = ["pip", "install", "--upgrade", package_name]
        else:
            # Install or upgrade the package with specific version
            command = ["pip", "install", "--force-reinstall", f"{package_name}=={package_version}"]

        logic.ci_print(f"Running command: {' '.join(command)}")

        try:
            # Run the command
            result = subprocess.run(command, capture_output=True, text=True)

            logic.ci_print(f"Command output: {result.stdout}")
            logic.ci_print(f"Command error: {result.stderr}")

            if result.returncode != 0:
                logic.ci_print(f"Command failed with exit status {result.returncode}")
                return


        except subprocess.CalledProcessError as e:
            # Print error message
            logic.handleError("update_and_run failed", e)
            logic.ci_print(f"Command failed with exit status {e.returncode}")
            logic.ci_print(f"stdout: {e.stdout}")
            logic.ci_print(f"stderr: {e.stderr}")
            return

        # Print success message
        logic.ci_print(f"Package {package_name}=={package_version} installed successfully")

        # Locate the installed package
        command2 = ["pip", "show", package_name]
        logic.ci_print(f"Running command2: {' '.join(command2)}")

        package_info = subprocess.check_output(command2).decode()
        package_location = None
        for line in package_info.splitlines():
            if line.startswith("Location:"):
                package_location = line.split(": ")[1]
                break



        if package_location is None:
            logic.ci_print("Could not determine the package location.")
            return

        # Construct the path to the installed package
        installed_package_path = package_location

        logic.ci_print('package_info: ' + package_info)
        logic.ci_print('installed_package_path: ' + installed_package_path)

        logic_source = os.path.join(installed_package_path, "logic.py")
        main_source = os.path.join(installed_package_path, "main.py")
        myservice_source = os.path.join(installed_package_path, "myservice.py")
        setup_source = os.path.join(installed_package_path, "setup.py")

        if not os.path.isfile(logic_source) or not os.path.isfile(main_source):
            print(f"logic.py or main.py not found in {installed_package_path}.")
            return

        # Copy files to the destination
        shutil.copy(logic_source, current_script_dir)
        shutil.copy(main_source, current_script_dir)
        shutil.copy(myservice_source, current_script_dir)
        shutil.copy(setup_source, current_script_dir)

        logic.ci_print(f"Copied logic.py, main.py, myservice.py, and setup.py to {current_script_dir}")

    except subprocess.CalledProcessError as e:
        logic.handleError(f"An error occurred during package update", e)


def upgrade_version(new_version="", current_version=""):
    try:
        logic.ci_print(f"Attempting to upgrade from version {current_version} to version {new_version}")
        update_and_run("main.py", "CI_CloudConnector", new_version)
        logic.ci_print("Upgrade successful.")

    except Exception as ex:
        logic.handleError("Error occurred during version upgrade: ", ex)


def MainLoopTimer():
    logic.ci_print(f"MainLoopTimer: {str(datetime.now())}", "INFO")

    global REPEATING_TIMER

    if REPEATING_TIMER:
        REPEATING_TIMER.stop()

    if SERVICE_STOP == 1:
        REPEATING_TIMER = None
        return

    try:
        MainLoop()
    except Exception as e:
        logic.handleError(f"Error occurred in MainLoopTimer", e)

    if REPEATING_TIMER:
        REPEATING_TIMER.start()
    else:
        REPEATING_TIMER = RepeatedTimer(5, MainLoopTimer)


def MainLoop():
    global SERVER_VERSION
    global UPGRADE_COUNTER

    try:
        # Get version and update if needed
        logic.get_cloud_version()
        local_ver = str(logic.getLocalVersion())
        update_to_ver = str(logic.getServerSugestedVersion())

        # To prevent upgrading too much in case of a problem, count upgrade attempts and stop when it's too big.
        # If the version changes, try again.
        if SERVER_VERSION != update_to_ver:
            SERVER_VERSION = update_to_ver
            UPGRADE_COUNTER = 0

        if str(update_to_ver) == "None":
            update_to_ver = ""

        if (bool(update_to_ver != "") & bool(update_to_ver != local_ver) & bool(UPGRADE_COUNTER < 10)):
            UPGRADE_COUNTER += 1
            logic.ci_print(
                f"Starting auto upgrade from: {local_ver} to: {update_to_ver}, Upgrade count: {UPGRADE_COUNTER}",
                "INFO")
            upgrade_version(update_to_ver, local_ver)

        logic.Main()
    except Exception as e:
        logic.handleError(f"Error occurred in MainLoop", e)


def StartMainLoop():
    global REPEATING_TIMER
    try:
        REPEATING_TIMER = RepeatedTimer(5, MainLoopTimer)
    except Exception as inst:
        logic.handleError("Error occurred in StartMainLoop", inst)


def args(argv):
    if len(argv) > 1 and argv[1] == "Start":
        StartMainLoop()


class MainFileChangeHandler(FileSystemEventHandler):
    def __init__(self, main_file, service):
        super().__init__()
        self.main_file = main_file
        self.myService = service

    def on_modified(self, event):

        try:
            if event.src_path.endswith(self.main_file):
                logic.ci_print("Main file has been modified. Signaling service to restart...")

                # Stop the service
                self.myService.ServiceUpdated()
                logic.ci_print("Service stopped. You may restart it if necessary.")

        except Exception as e:
            logic.handleError(f"Error occurred during file modification event handling", e)

def monitor_main_file(main_file, service):
    try:
        observer = Observer()

        event_handler = MainFileChangeHandler(os.path.basename(main_file), service)
        observer.schedule(event_handler, path=os.path.dirname(main_file), recursive=False)

        observer.start()
        logic.ci_print(f"Monitoring main file: {main_file}")

        return observer

    except Exception as e:
        logic.handleError(f"Error occurred while setting up file monitoring", e)
        return None


def serviceStop():
    global SERVICE_STOP
    SERVICE_STOP = 1
    logic.ci_print("Service stop requested.")


def set_service_restart_delay(service_name, delay_milliseconds):
    command = f'sc failure {service_name} reset= 0 actions= restart/{delay_milliseconds}'
    try:
        subprocess.run(command, shell=True, check=True)
        logic.ci_print(f"Restart delay for service '{service_name}' set to {delay_milliseconds} milliseconds.")
    except subprocess.CalledProcessError as e:
        logic.ci_print(f"Error setting restart delay for service '{service_name}': {e}")


def set_service_startup_type(service_name, startup_type):
    """
    Set the startup type for a Windows service.

    Args:
        service_name (str): The name of the service.
        startup_type (str): The startup type to set ('auto', 'demand', 'disabled', 'delayed-auto').

    Returns:
        bool: True if the command is executed successfully, False otherwise.
    """
    try:
        subprocess.run(['sc', 'config', service_name, 'start=' + startup_type], check=True, shell=True)
        logic.ci_print(f"Service '{service_name}' startup type set to '{startup_type}'.")
    except subprocess.CalledProcessError as e:
        logic.handleError(f"Failed to set service startup type. Error: {e}")


def init():
    logic.initialize_config()
    set_service_restart_delay("CI_PlantSharpEdgeGateway", 10000)
    set_service_startup_type("CI_PlantSharpEdgeGateway", "auto")


if __name__ == '__main__':
    init()
    args(sys.argv)
    #args([0, 'Start'])
    main_file = "logic.py"
    monitor_main_file(main_file)