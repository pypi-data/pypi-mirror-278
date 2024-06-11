import logging, time, datetime, sys, socket, random, tzlocal, glob, fnmatch
import platform
from collections import deque
from datetime import datetime
from cpppo.server.enip import address, client
import os
import configparser
import requests
import json

VERSION = "4.1"

# config
CONFIG_SERVER_ADDRESS = ""
CONFIG_USERNAME = ""
CONFIG_PASSWORD = ""
CONFIG_LOG_LEVEL = ""

TAGS_DEFINITION_FILE_NAME = "TagsDefinition.txt"
GET_TAGS_FROM_SERVER_MIN_RATE_SECONDS = 10
GET_CLOUD_VERSION_FROM_SERVER_MIN_RATE_SECONDS = 10
VERIFY_SSL = False  # True = do not allow un verified connection , False = Allow

SUGGESTED_UPDATE_VERSION = ""
CONFIG_FILE = "config.ini"
SCAN_RATE_LAST_READ = {}
CURRENT_TOKEN = ""
CONNECTOR_TYPE_NAME = ""
LAST_GET_TAGS_FROM_SERVER = None
LAST_GET_CLOUD_VERSION_FROM_SERVER = None

def enum(**enums):
    return type("Enum", (), enums)

TagStatus = enum(Invalid=10, Valid=20)

# Retrieve the logger instance
logger = logging.getLogger(__name__)


# ============================
def read_last_rows_from_log(max_number_of_rows=10):
    log_file_path = "PlantSharpEdgeGateway.log"
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as file:
            last_rows = deque(file, maxlen=max_number_of_rows)

        return list(map(str.rstrip, last_rows))
    return None

# ============================

def set_log_level(lvl):
    global logger

    try:
        lvl = str(lvl).upper()

        if lvl == "CRITICAL":
            logger.setLevel(logging.CRITICAL)
        if lvl == "ERROR":
            logger.setLevel(logging.ERROR)
        if lvl == "WARNING":
            logger.setLevel(logging.WARNING)
        if lvl == "INFO":
            logger.setLevel(logging.INFO)
        if lvl == "DEBUG":
            logger.setLevel(logging.DEBUG)
        if lvl == "NOTSET":
            logger.setLevel(logging.NOTSET)

    except Exception as inst:
        handleError("Error in set_log_level", inst)


# ============================
def ci_print(msg, level=""):
    global logger
    try:
        if level == "DEBUG":
            logger.debug(msg)
        elif level == "INFO":
            logger.info(msg)
        elif level == "ERROR":
            logger.error(msg)
        elif level == "WARNING":
            logger.warning(msg)
        else:
            logger.info(msg)

    except Exception as e:
        logger.warning(f"An error occurred while logging: {e}")


# ============================
def SendLogToServer(log):
    try:
        addCloudConnectorLog(log, datetime.now())
        return
    except Exception as e:
        return


# ============================
def handleError(message, err):
    try:

        err_desc = str(err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.basename(exc_tb.tb_frame.f_code.co_filename)
        srtMsg = (
            f"{message} , {err_desc} , {exc_type} , {fname} , {exc_tb.tb_lineno}"
        )
        ci_print(srtMsg, "ERROR")
    except Exception as inner_err:
        ci_print(f"Error in handleError: {inner_err}", "ERROR")


# ============================
def getAliveFile():
    ret = None
    try:
        file_path = "lc_pid.txt"
        with open(file_path, "r") as file:
            ret = json.load(file)
    except Exception as e:
        handleError("Error reading alive file: %s", e)
    return ret


# ============================
def initialize_config(overwrite=False):

    global CONFIG_SERVER_ADDRESS
    global CONFIG_USERNAME
    global CONFIG_PASSWORD
    global CONFIG_LOG_LEVEL

    try:
        file_path = f"{CONFIG_FILE}"

        if os.path.exists(file_path) and not overwrite:
            config = configparser.ConfigParser()
            config.read(file_path)

            CONFIG_SERVER_ADDRESS = config.get("Server", "Address")
            CONFIG_USERNAME = config.get("Server", "username")
            CONFIG_PASSWORD = config.get("Server", "password")
            CONFIG_LOG_LEVEL = config.get("Logging", "Level", fallback=CONFIG_LOG_LEVEL)


            ci_print("Reading configuration file...", "INFO")
            ci_print(f"Server Address: {CONFIG_SERVER_ADDRESS}", "INFO")
            ci_print(f"Username: {CONFIG_USERNAME}", "INFO")
            ci_print(f"Password: {CONFIG_PASSWORD}", "INFO")
            ci_print(f"Log Level: {CONFIG_LOG_LEVEL}", "INFO")
            ci_print(f"VERSION: {getLocalVersion()}")

            set_log_level(CONFIG_LOG_LEVEL)
        else:
            ci_print(
                f"No existing configuration found or overwrite is set to True. Creating a new configuration file at {file_path}",
                "INFO")

            config = configparser.ConfigParser()
            config.add_section("Server")
            config.add_section("Logging")

            def get_input(prompt, current_value):
                value = input(prompt + f" (Currently: {current_value}): ")
                return value if value else current_value

            CONFIG_SERVER_ADDRESS = get_input("Enter Server Address (e.g., https://localhost:63483)", CONFIG_SERVER_ADDRESS)
            CONFIG_USERNAME = get_input("Enter new user name", CONFIG_USERNAME)
            CONFIG_PASSWORD = get_input("Enter password", CONFIG_PASSWORD)
            CONFIG_PASSWORD = get_input(f"Enter Logging Level [DEBUG , INFO , WARNING , ERROR]", CONFIG_PASSWORD)


            config.set("Server", "Address", CONFIG_SERVER_ADDRESS)
            config.set("Server", "username", CONFIG_USERNAME)
            config.set("Server", "password", CONFIG_PASSWORD)
            config.set("Logging", "Level", CONFIG_PASSWORD)


            with open(file_path, "w") as configfile:
                config.write(configfile)

            ci_print("Configuration file created successfully.", "INFO")

            initialize_config()  # Reload the config after updating

    except Exception as inst:
        handleError("An error occurred during configuration initialization", inst)


# ============================
def reboot():

    try:
        if platform.system() == "Windows":
            ci_print("Reboot not supported on Windows.", "INFO")
            #subprocess.run(["shutdown", "/r", "/t", "0"], check=True)
        else:
            ci_print("Reboot not supported on !Windows.", "INFO")
            #os.system("sudo reboot")
    except Exception as ex:
        handleError("Error in reboot", ex)


# Cloud Functions
# ============================

CONFIG_SERVER_ADDRESS = "your_server_address"
VERIFY_SSL = True
CURRENT_TOKEN = ""
CONFIG_USERNAME = "your_username"
CONFIG_PASSWORD = "your_password"
CONFIG_LOG_LEVEL = "INFO"

def get_cloud_token():

    global CONFIG_SERVER_ADDRESS
    global VERIFY_SSL
    global CURRENT_TOKEN

    if CURRENT_TOKEN:
        ci_print("Using cached token.", "INFO")
        return CURRENT_TOKEN

    url = f"{CONFIG_SERVER_ADDRESS}/api/CloudConnector/Token"

    try:
        response = requests.post(
            url,
            data={
                "grant_type": "password",
                "username": CONFIG_USERNAME,
                "password": CONFIG_PASSWORD,
            },
            headers={
                "User-Agent": "python",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            verify=VERIFY_SSL,
        )

        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.text

        jsonData = json.loads(data)
        token = jsonData.get("access_token", "")

        if token:
            CURRENT_TOKEN = token
            ci_print("Token received successfully from the server.", "INFO")

    except requests.exceptions.RequestException as e:
        handleError("Error occurred while getting the token", e)
        token = ""
    except json.JSONDecodeError as e:
        handleError("Error decoding token response", e)
        token = ""
    except KeyError as e:
        handleError("Token not found in response", e)
        token = ""

    return token


# ============================
# make http request to cloud if fails set CURRENT_TOKEN='' so it will be initialized next time
# ============================
def ciRequest(url, data, method="get", action="", token=""):

    result = {"success": False}
    global CURRENT_TOKEN

    if not token:
        ci_print(f"Skipping {action} - no Token", "INFO")
        return result

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "text/plain"
    }

    if method.lower() == "post":
        headers["Content-Type"] = "application/json"

    try:
        if method.lower() == "post":
            ci_print(f"ciRequest: Sending POST request to {url} for {action}. Data: {data}", "INFO")
            response = requests.post(url, data=data, headers=headers, verify=VERIFY_SSL)
        else:
            ci_print(f"ciRequest: Sending GET request to {url} for {action}.", "INFO")
            response = requests.get(url, headers=headers, verify=VERIFY_SSL)

        ci_print(f"ciRequest: Received response from {url} - Status code: {response.status_code}.", "INFO")


        #403 Forbidden 401 Unauthorized 503 Server Unavailable
        if response.status_code == 403 or response.status_code == 503 or response.status_code == 401:
            ci_print(f"ciRequest: Token invalidated due to status code {response.status_code}.", "INFO")
            CURRENT_TOKEN = ""

        result["success"] = response.status_code == 200
        result["response"] = response

    except Exception as err:
        handleError(f"Error occurred in ciRequest for {action}", err)
        CURRENT_TOKEN = ""

    return result


# ============================
def get_cloud_version():

    global GET_CLOUD_VERSION_FROM_SERVER_MIN_RATE_SECONDS
    global LAST_GET_CLOUD_VERSION_FROM_SERVER
    global CURRENT_TOKEN
    global VERSION
    global SUGGESTED_UPDATE_VERSION

    if not CURRENT_TOKEN:
        CURRENT_TOKEN = get_cloud_token()

    token = CURRENT_TOKEN

    tags = None

    try:
        now = datetime.now()
        time_since_last_check = 0

        # Calculate the time passed since the last version check
        if LAST_GET_CLOUD_VERSION_FROM_SERVER:
            time_since_last_check = (now - LAST_GET_CLOUD_VERSION_FROM_SERVER).total_seconds()

        # Check if enough time has passed since the last version check
        if time_since_last_check == 0 or time_since_last_check > GET_CLOUD_VERSION_FROM_SERVER_MIN_RATE_SECONDS:
            handle_new_requests()
            LAST_GET_CLOUD_VERSION_FROM_SERVER = datetime.now()

            ip_address = socket.gethostbyname(socket.gethostname())
            url = f"{CONFIG_SERVER_ADDRESS}/api/CloudConnector/GetVersion/?version={VERSION}&IpAddress={ip_address}"

            ci_print(f"Requesting cloud version information from {url}", "INFO")

            ret = ciRequest(url, None, "get", "getCloudVersion", token)
            response = ret["response"]
            success = ret["success"]

            if not success:
                return ""

            server_response = json.loads(response.text)
            suggested_version = server_response[0]
            SUGGESTED_UPDATE_VERSION = suggested_version

            ci_print(f"Received cloud version information. Suggested update version: {suggested_version}", "INFO")

            ans = json.loads(response.text)
            update_to_version = ans[0]

            SUGGESTED_UPDATE_VERSION = update_to_version

            if suggested_version and suggested_version != VERSION:
                ci_print(f"Local Version: {VERSION}, but Server suggests: {suggested_version}", "INFO")


    except Exception as e:
        handleError("Error occurred while getting version from cloud", e)
        SUGGESTED_UPDATE_VERSION = ""

    return SUGGESTED_UPDATE_VERSION


# ============================
def get_cloud_tags(token=""):
    global LAST_GET_TAGS_FROM_SERVER
    global GET_TAGS_FROM_SERVER_MIN_RATE_SECONDS

    tags = None
    try:
        url = f"{CONFIG_SERVER_ADDRESS}/api/CloudConnector/GetTags/"
        now = datetime.now()
        elapsed_time_since_last_fetch = 0

        if LAST_GET_TAGS_FROM_SERVER:
            elapsed_time_since_last_fetch = (now - LAST_GET_TAGS_FROM_SERVER).total_seconds()

        if elapsed_time_since_last_fetch == 0 or elapsed_time_since_last_fetch > GET_TAGS_FROM_SERVER_MIN_RATE_SECONDS:
            ci_print(f"Fetching tags from {url}", "INFO")
            response_data = ciRequest(url, None, "get", "getCloudTags", token)

            if response_data and response_data["success"]:
                response = response_data["response"]
                LAST_GET_TAGS_FROM_SERVER = now
                tags_data = json.loads(response.text)
                arranged_tags = arrange_tags_by_scan_time(tags_data["Tags"])
                tags = {"Tags": arranged_tags}

                ci_print("Successfully retrieved tags from Cloud server.", "INFO")

                with open(TAGS_DEFINITION_FILE_NAME, "w") as file:
                    json.dump(tags, file)
                    ci_print(f"Tags saved to {TAGS_DEFINITION_FILE_NAME}", "INFO")
            else:
                ci_print("Failed to retrieve Tags from Cloud server", "WARNING")

    except Exception as error:
        handleError("Error occurred while getting tags from cloud", error)
        tags = None

    if tags is None:
        ci_print("Loading tags from local file due to previous error.", "WARNING")
        tags = get_tags_definition_from_file()

    return tags


# ============================
def arrange_tags_by_scan_time(tags):
    ans = {}

    try:
        for index in range(len(tags)):
            scan_rate = tags[index]["ScanRate"]

            if scan_rate in ans:
                tagsListPerScanRate = ans[scan_rate]
            else:
                ans[scan_rate] = []

            ans[scan_rate].append(tags[index])
    except Exception as err:
        handleError("Error arranging tags by scan time", err)
    return ans


# ============================
def printTags(tags):
    try:
        ci_print(str(tags))

        for tag in tags:
            tag_id = tag.get("TagId", "")
            tag_name = tag.get("TagName", "")
            tag_address = tag.get("TagAddress", "")
            scan_rate = tag.get("ScanRate", "")

            msg = f"Tag Id: {tag_id}, TagName: {tag_name}, TagAddress: {tag_address}, ScanRate: {scan_rate}"
            ci_print(msg, "INFO")

    except Exception as inst:
        handleError("Error in printTags", inst)


# ============================
def set_cloud_tags(tag_values, token=""):
    global TagStatus
    updated_successfully = False

    try:
        url = f"{CONFIG_SERVER_ADDRESS}/api/CloudConnector/SetCounterHistory/"
        payload = []

        for tag in tag_values:
            tag_id = tag.get("TagId")
            timestamp = str(tag.get("time"))
            value = tag.get("value")
            status = TagStatus.Valid if str(tag.get("status")) == "20" else TagStatus.Invalid

            tag_val = {
                "TagId": tag_id,
                "TimeStmp": timestamp,
                "StatusCE": status,
                "Value": value,
            }
            payload.append(tag_val)

        ci_print(f"Sending tags to {url}. Payload: {json.dumps(payload, indent=2)}", "INFO")
        ret = ciRequest(url, json.dumps(payload), "post", "setCloudTags", token)
        updated_successfully = ret["success"]

        if updated_successfully:
            ci_print("Tags successfully updated in the cloud.", "INFO")
        else:
            ci_print("Failed to update tags in the cloud.", "WARNING")

    except Exception as inst:
        handleError("Error occurred while setting tags in the cloud", inst)
        return False

    return updated_successfully


# ============================
def send_log_file_to_cloud(numberOfRows=10, timestamp="", requestId=""):
    try:
        requestId = str(requestId)
        lines = read_last_rows_from_log(numberOfRows)
        for line in lines:
            addCloudConnectorLog(line, timestamp, str(requestId))
    except Exception as inst:
        handleError("Error occurred while sending log file to cloud", inst)
        return False


# ============================
def addCloudConnectorLog(log, timestamp="", request_id=""):

    global CURRENT_TOKEN
    if not timestamp:
        timestamp = datetime.now()

    token = CURRENT_TOKEN
    if not token:
        return False


    try:
        url = CONFIG_SERVER_ADDRESS + "/api/CloudConnector/SetCounterLog/"

        payload = [{"Log": log, "TimeStamp": str(timestamp), "RequestId": request_id}]
        ret = ciRequest(url, json.dumps(payload), "post", "SetConnectorLog", token)
        return ret["success"]

    except Exception as inst:
        handleError("Exception in addCloudConnectorLog", inst)
        return False


# ============================
def fetch_cloud_connector_requests():
    global CURRENT_TOKEN
    token = CURRENT_TOKEN

    requests_data = None
    try:
        url = f"{CONFIG_SERVER_ADDRESS}/api/CloudConnector/GetCloudConnectorRequests/"
        response_data = ciRequest(url, None, "get", "GetCloudConnectorRequests", token)

        if response_data and response_data["success"]:
            response = response_data["response"]
            requests_data = json.loads(response.text)

    except Exception as error:
        handleError("Error fetching requests from cloud", error)
        requests_data = None

    return requests_data


# ============================
def update_cloud_connector_request_status(requestId, status):

    global CURRENT_TOKEN
    updatedSuccessfully = False

    token = CURRENT_TOKEN
    if not token:
        ci_print("no token skip updateCloudConnectorRequests", "WARNING")
        return
    try:
        url = (
            CONFIG_SERVER_ADDRESS
            + "/api/CloudConnector/SetCounterRequestStatus/?requestId="
            + str(requestId)
            + "&status="
            + str(status)
        )

        ret = ciRequest(url, "", "post", "SetCounterRequestStatus", token)
        updatedSuccessfully = ret["success"]

    except Exception as inst:
        handleError("Exception in addCloudConnectorLog", inst)
        return False

    return updatedSuccessfully


# get requests from cloud and handle it
# ============================
def handle_new_requests():

    try:
        requests = fetch_cloud_connector_requests()
        if requests:
            for request in requests:
                try:

                    request_id = request["Id"]
                    request_type = request["Type"]
                    request_data = json.loads(request["Data"])

                    if request_type == 1:  # Send logs
                        ci_print(f"Handling send log request: {request}", "INFO")
                        row_count = request_data["Rows"]
                        update_cloud_connector_request_status(request_id, 2)  # In process
                        send_log_file_to_cloud(row_count, "", request_id)
                        update_cloud_connector_request_status(request_id, 3)  # Done

                    elif request_type == 2:  # Change logs level
                        ci_print(f"Handling change log level request: {request}", "INFO")
                        new_log_level = request_data["Level"]
                        update_cloud_connector_request_status(request_id, 2)  # In process
                        set_log_level(new_log_level)
                        update_cloud_connector_request_status(request_id, 3)  # Done

                    elif request_type == 3:  # Reboot
                        ci_print(f"Handling reboot request: {request}", "INFO")
                        update_cloud_connector_request_status(request_id, 3)  # Done
                        reboot()

                except Exception as inner_error:
                    handleError("Error processing individual request in handle_new_requests", inner_error)
    except Exception as outer_error:
        handleError("Error in handle_new_requests", outer_error)
        return False


# ============================
# PLC Functions
# ============================
def fill_Invalids(tags_definitions, values):
    global TagStatus

    ret_values = []
    try:
        time = str(datetime.now(tzlocal.get_localzone()))
        values_dictionary = {}

        for value in values:
            values_dictionary[value["TagId"]] = value

        for tag in tags_definitions:
            TagId = tag["TagId"]
            if TagId in values_dictionary:
                ret_values.append(values_dictionary[TagId])
            else:
                tagAddress = tag["TagAddress"]
                val = {
                    "TagAddress": tagAddress,
                    "TagId": TagId,
                    "time": time,
                    "value": None,
                    "status": TagStatus.Invalid,
                }
                ret_values.append(val)
    except Exception as inst:
        handleError("Error in fill_Invalids", inst)

    return ret_values


# ippp
# ============================
def readEtherNetIP_Tags(tags_definitions):

    global TagStatus
    ci_print("Starting readEtherNetIP_Tags", "INFO")
    ans = []

    arranged_tags = arrange_tags_by_plc(tags_definitions)

    try:

        for plc_address, tags_def_list in arranged_tags.items():
            tags = [tag_def["TagAddress"] for tag_def in tags_def_list]
            ci_print(f"readEtherNetIP_Tags: Reading tags from PLC {plc_address}: {tags}", "DEBUG")

            with client.connector(host=plc_address, port=address[1], timeout=1.0) as connection:
                operations = client.parse_operations(tags)
                failures, transactions = connection.process(
                    operations=operations,
                    depth=1,
                    multiple=0,
                    fragment=False,
                    printing=False,
                    timeout=1.0,
                )

            #host = plc_address  # Controller IP address
            #port = address[1]  # default is port 44818
            #depth = 1  # Allow 1 transaction in-flight
            #multiple = 0  # Don't use Multiple Service Packet
            #fragment = False  # Don't force Read/Write Tag Fragmented
            #timeout = 1.0  # Any PLC I/O fails if it takes > 1s
            #printing = False  # Print a summary of I/O

            ci_print(f"Transactions: {transactions}", "INFO")
            ci_print(f"Failures: {failures}", "INFO")


            # client.close()
            # sys.exit( 1 if failures else 0 )

            for index, tag_def in enumerate(tags_def_list):
                tag_address = tag_def["TagAddress"]
                try:
                    if transactions[index]:
                        tag_id = int(tag_def["TagId"])
                        value = transactions[index][0]
                        time = str(datetime.now(tzlocal.get_localzone()))
                        ci_print(f"Successfully read tag. Address: {tag_address}, Value: {value}", "INFO")

                        val = {
                            "TagAddress": tag_address,
                            "TagId": tag_id,
                            "time": time,
                            "value": value,
                            "status": TagStatus.Valid,
                        }
                        ans.append(val)
                    else:
                        ci_print(f"Error reading tag {tag_address}: No transaction data", "WARNING")
                except ValueError as ve:
                    handleError(f"ValueError reading tag {tag_address}", ve)

        ci_print("Finished reading EtherNetIP Tags", "INFO")
    except Exception as inst:
        handleError("Error in readEtherNetIP_Tags", inst)

    return fill_Invalids(tags_definitions, ans)


def arrange_tags_by_plc(tags_definitions):

    arranged_tags = {}

    for tag_def in tags_definitions:
        plc_address = tag_def.get("PlcIpAddress")
        if plc_address:
            if plc_address not in arranged_tags:
                arranged_tags[plc_address] = []
            arranged_tags[plc_address].append(tag_def)

    return arranged_tags

# ============================
def readModBusTags(tags_definitions):

    ans = []

    arranged_tags = arrange_tags_by_plc(tags_definitions)

    try:
        ci_print("Starting readModBusTags", "INFO")

        for plc_address, tags_def_list in arranged_tags.items():
            ci_print(f"Connecting to PLC at {plc_address}", "INFO")
            maxOffset = 0

            for p in tags_def_list:
                offset = int(p["TagAddress"])
                maxOffset = max(maxOffset, offset)

            from pymodbus.client import ModbusTcpClient as ModbusClient

            client = ModbusClient(plc_address, port=502)
            client.connect()

            ci_print(f"Connected to PLC at {plc_address}", "INFO")

            rr = client.read_input_registers(0, maxOffset) # 30000
            ci_print(f"Read input registers: {rr.registers}", "INFO")

            for tag_def in tags_def_list:
                try:
                    offset = int(tag_def["TagAddress"]) - 1
                    tag_id = int(tag_def["TagId"])

                    value = rr.registers[offset]
                    time = str(datetime.now(tzlocal.get_localzone()))
                    ci_print(f"Read tag {tag_def['TagAddress']} at offset {offset} with value {value}", "INFO")

                    val = {
                        "TagAddress": tag_def["TagAddress"],
                        "TagId": tag_id,
                        "time": time,
                        "value": value,
                        "status": TagStatus.Valid,
                    }
                    ans.append(val)
                except ValueError as ve:
                    handleError(f"ValueError reading tag {tag_def['TagAddress']}", ve)
                except IndexError as ie:
                    handleError(f"IndexError reading tag {tag_def['TagAddress']}", ie)

            client.close()
            ci_print(f"Disconnected from PLC at {plc_address}", "INFO")

        ci_print("Finished reading ModBus Tags", "INFO")
        return ans
    except Exception as inst:
        handleError("Error in readModBusTags", inst)
        return fill_Invalids(tags_definitions, ans)


# ============================
mynumber = 1

def readSimulation_Tags(tags_definitions):
    global mynumber
    ans = []
    arranged_tags = arrange_tags_by_plc(tags_definitions)

    ci_print("Starting readSimulation_Tags", "INFO")

    try:

        for plc_address, tags_def_list in arranged_tags.items():
            ci_print(f"Processing PLC at address: {plc_address}", "INFO")

            for index, tag_def in enumerate(tags_def_list):
                try:
                    tag_id = int(tag_def.get("TagId"))
                    value = random.uniform(-10, 10)
                    value = mynumber
                    mynumber = mynumber +1

                    time = str(datetime.now(tzlocal.get_localzone()))
                    val = {
                        "TagId": tag_id,
                        "time": time,
                        "value": value,
                        "status": TagStatus.Valid,
                    }
                    ans.append(val)

                    ci_print(
                        f"PLC Address: {plc_address}, TagId: {tag_id}, Value: {value}, "
                        f"ScanRate: {tag_def.get('ScanRate')}", "DEBUG"
                    )


                except (ValueError, TypeError) as e:
                    handleError(f"Error processing tag definition for PLC {plc_address}, TagId: {tag_def.get('TagId')}", e)


    except Exception as inst:
        handleError("Error in readSimulation_Tags", inst)

    ci_print("Finished readSimulation_Tags", "INFO")
    return ans


# ============================
def printTagValues(tagValues):
    ci_print("Count " + str(len(tagValues)) + " Tags", "INFO")
    for index in range(len(tagValues)):
        ci_print(str(tagValues[index]), "INFO")


# ============================
def getLocalVersion():
    return VERSION


# ============================
def getServerSugestedVersion():
    return SUGGESTED_UPDATE_VERSION


# ============================
# Tag Files Functions
# ============================

def write_tags_definition_to_file(tags):
    ci_print(f"Starting to write tags definition to file: {TAGS_DEFINITION_FILE_NAME}", "INFO")

    try:
        with open(TAGS_DEFINITION_FILE_NAME, "w") as f:
            json.dump(tags, f)

        ci_print(f"Successfully wrote tags definition to file: {TAGS_DEFINITION_FILE_NAME}", "INFO")
    except Exception as e:
        handleError(f"Failed to write tags definition to file: {TAGS_DEFINITION_FILE_NAME}", e)

# ============================

def get_tags_definition_from_file():
    ci_print(f"Starting to read tags definition from file: {TAGS_DEFINITION_FILE_NAME}", "INFO")
    try:
        with open(TAGS_DEFINITION_FILE_NAME, "r") as f:
            tags = json.load(f)
        ci_print(f"Successfully read tags definition from file: {TAGS_DEFINITION_FILE_NAME}", "INFO")
        return tags
    except FileNotFoundError as e:
        handleError(f"File not found: {TAGS_DEFINITION_FILE_NAME}. Returning empty tags definition.", e)
        return {}
    except json.JSONDecodeError as e:
        handleError(f"Error decoding JSON from file: {TAGS_DEFINITION_FILE_NAME}. Returning empty tags definition.", e)
        return {}
    except Exception as e:
        handleError(f"Failed to read tags definition from file: {TAGS_DEFINITION_FILE_NAME}", e)
        return {}


# ============================


def get_tags_values_from_file(file_path):
    ci_print(f"Starting to read tag values from file: {file_path}", "INFO")
    try:
        with open(file_path, "r") as file:
            values = json.load(file)
        ci_print(f"Successfully read tag values from file: {file_path}", "INFO")
        return values
    except FileNotFoundError as e:
        handleError(f"File not found: {file_path}. Returning empty dictionary.", e)
        return {}
    except json.JSONDecodeError as e:
        handleError(f"Error decoding JSON from file: {file_path}. Returning empty dictionary.", e)
        return {}
    except Exception as e:
        handleError(f"Failed to read tag values from file: {file_path}", e)
        return {}


# ============================

def save_values_to_file(values, file_name=None):
    if file_name is None:
        file_name = "[NEW]TagsValuesFile" + datetime.now().strftime("%Y%m%d-%H%M%S%f") + ".txt"

    ci_print(f"Starting to save values to file: {file_name}", "INFO")

    try:
        with open(file_name, "w") as f:
            json.dump(values, f)
        ci_print(f"Successfully saved values to file: {file_name}", "INFO")
        time.sleep(1)

    except Exception as inst:
        handleError(f"Error saving values to file: {file_name}.", inst)




# ============================
def handle_values_file(file_name, token=""):
    ci_print(f"Handling values file: {file_name}", "INFO")
    try:
        values = get_tags_values_from_file(file_name)
        if values:
            success = set_cloud_tags(values, token)
            if success:
                os.remove(file_name)
                ci_print(f"Successfully processed and removed file: {file_name}", "INFO")
                return True
            else:
                ci_print(f"Failed to set cloud tags for file: {file_name}", "ERROR")
                # Create error directory if it does not exist
                err_dir = os.path.join(os.path.dirname(file_name), "ERR")
                if not os.path.exists(err_dir):
                    os.makedirs(err_dir)

                # Construct the new error file path
                base_name = os.path.basename(file_name)
                err_file = os.path.join(err_dir, base_name.replace("[NEW]", "[ERR]"))

                # Rename (move) the file to the error directory
                os.rename(file_name, err_file)
                ci_print(f"Moved file to error directory: {err_file}", "INFO")
    except FileNotFoundError as e:
        handleError(f"File not found: {file_name}.", e)
    except Exception as e:
        handleError(f"Error processing file: {file_name}.", e)

    return False

# ============================
def handle_all_values_files(token=""):
    ci_print("Handling all values files in the directory", "INFO")
    try:
        dir_path = os.getcwd()
        files_starting_with_tags_values_file = [
            file for file in os.listdir(dir_path) if file.startswith("[NEW]TagsValuesFile")
        ]

        if not files_starting_with_tags_values_file:
            ci_print("No files found matching the pattern '[NEW]TagsValuesFile' in the directory.", "INFO")
            return

        files_starting_with_tags_values_file.sort(key=lambda s: os.path.getmtime(os.path.join(dir_path, s)))

        for file in files_starting_with_tags_values_file:
            if file.endswith(".txt") and file.startswith("[NEW]"):
                handle_values_file(os.path.join(dir_path, file), token)

        ci_print("Completed handling all values files in the directory", "INFO")
    except Exception as e:
        handleError("Error occurred while handling all values files in the directory.", e)


def arrange_by_connector_type(tags_def):
    arranged_tags = {}

    for tag in tags_def:
        connector_type = tag.get('connectorTypeName', '')
        if connector_type not in arranged_tags:
            arranged_tags[connector_type] = []
        arranged_tags[connector_type].append(tag)

    return arranged_tags

# ============================
# Main Loop
# ============================
def Main():
    ci_print("Starting Main", "INFO")
    global SCAN_RATE_LAST_READ
    global CURRENT_TOKEN

    try:

        if not CURRENT_TOKEN:
            CURRENT_TOKEN = get_cloud_token()

        # Fetch cloud tags definition and scan rates
        tags_def_scan_rates_response = get_cloud_tags(CURRENT_TOKEN)
        tags_def_scan_rates = tags_def_scan_rates_response["Tags"]

        for scan_rate in tags_def_scan_rates:
            if scan_rate in (None, 'null'):
                continue

            scan_rate_int = int(scan_rate)
            scan_rate_str = str(scan_rate)
            diff = 0

            # Calculate the time difference since the last read
            if scan_rate_str in SCAN_RATE_LAST_READ:
                now = datetime.now()
                diff = (now - SCAN_RATE_LAST_READ[scan_rate_str]).total_seconds()

            # Proceed if the time difference exceeds the scan rate or if this is the first read
            if diff + 3 > scan_rate_int or diff == 0:
                tags_def = tags_def_scan_rates[scan_rate]
                arranged_tags = arrange_by_connector_type(tags_def)

                for connector_type, tags in arranged_tags.items():
                    values = None

                    # Read tags based on the connector type
                    if connector_type == "Simulation":
                        values = readSimulation_Tags(tags)
                    elif connector_type == "Modbus":
                        values = readModBusTags(tags)
                    elif connector_type == "Ethernet/IP":
                        values = readEtherNetIP_Tags(tags)

                        # Retry reading Ethernet/IP tags if no values are returned
                        if not values:
                            for retry_count in range(3):
                                time.sleep(0.3 * (retry_count + 1))
                                ci_print(f"Retry {retry_count + 1} reading Ethernet/IP tags. Empty Values", "ERROR")
                                values = readEtherNetIP_Tags(tags)
                                if values:
                                    break


                    # Save the read values to a file and update the last read time
                    if values:
                        save_values_to_file(values, None)
                        SCAN_RATE_LAST_READ[scan_rate_str] = datetime.now()

        # Handle all value files if a valid token is available
        if CURRENT_TOKEN:
            handle_all_values_files(CURRENT_TOKEN)
        else:
            ci_print("No Token available, skipping upload step", "WARNING")
    except Exception as e:
        handleError("Error occurred in Main.", e)
        CURRENT_TOKEN = ""
    finally:
        ci_print("Main function completed.", "INFO")
