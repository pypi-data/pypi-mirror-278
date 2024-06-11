import logging
import os
import time
import subprocess
import win32api
import win32con
import win32serviceutil
import win32service
import win32event
import main
from logging.handlers import RotatingFileHandler

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "CI_PlantSharpEdgeGateway"
    _svc_display_name_ = "CI_PlantSharpEdgeGateway"
    _svc_failure_actions_ = "restart/10000"  # Restart the service after 1 minute if it fails

    def __init__(self, args):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s: %(name)s: %(funcName)s: (%(lineno)d): %(levelname)s: %(message)s',
        )

        rotating_handler = RotatingFileHandler(
            filename='PlantSharpEdgeGateway.log',
            mode="a",
            maxBytes=5 * 1024 * 1024,
            backupCount=10,
            encoding=None,
            delay=0,
        )

        rotating_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s: %(name)s: %(funcName)s: (%(lineno)d): %(levelname)s: %(message)s')
        rotating_handler.setFormatter(formatter)

        logging.getLogger().addHandler(rotating_handler)

        # Now initialize other attributes
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.logger = logging.getLogger(__name__)


    def SvcDoRun(self):
        self.logger.info("Service is starting.")
        try:

            main.init()
            main.args([0, 'Start'])

            self.logger.info("Main application initialized.")

            python_exe_dir = get_python_executable_directory()

            logic_file =  f"{python_exe_dir}\\logic.py"
            observer = main.monitor_main_file(logic_file, self)

            self.logger.info(f"Monitoring file: {logic_file}")

            try:
                while main.SERVICE_STOP == 0:
                    time.sleep(1)
                self.logger.info("Service execution loop ended.")
            except KeyboardInterrupt:
                pass
            finally:
                observer.stop()
                observer.join()
                self.logger.info("Observer has been stopped.")

        except Exception as e:
            self.logger.error(f"Exception in SvcDoRun: {e}")

        # Wait for the stop event
        wait_result = win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
        if wait_result == win32event.WAIT_OBJECT_0:
            self.logger.info("Stop event signaled. Service is stopping.")
            return

    def SvcStop(self):
        try:
            self.logger.info("Service stop requested.")

            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)

            main.serviceStop()
            time.sleep(2)  # Allow some time for the service to stop gracefully

            win32event.SetEvent(self.stop_event)

            self.logger.info("Service stop event signaled.")
        except Exception as e:
            self.logger.error(f"Error occurred during service stop: {e}")

    def ServiceUpdated(self):
        self.logger.info('Service updated, stopping service...')
        self.SvcStop()
        os._exit(1)


    def SvcTerminate(self):
        time.sleep(1)  # Adjust the delay time as needed
        pid = self.GetPID()
        self.TerminateProcess(pid)
        win32event.SetEvent(self.stop_event)

    def GetPID(self):
        return win32api.GetCurrentProcessId()

    def TerminateProcess(self, pid):
        try:
            hProcess = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, pid)
            win32api.TerminateProcess(hProcess, 0)
            win32api.CloseHandle(hProcess)

            self.logger.info(f"Process {pid} terminated successfully.")

        except Exception as e:
            self.logger.error(f"Exception in TerminateProcess: {e}")

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)



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
                return ''

        else:
            return ''

    except subprocess.CalledProcessError as cpe:
        return ''
    except Exception as e:
        return ''

