import datetime
import json
from json import JSONEncoder

import ActionStreamer
from ActionStreamer import CommonFunctions

class PatchOperation:

    def __init__(self, field_name, value):
        self.field_name = field_name
        self.value = value
        
class WebServiceResult:

    def __init__(self, code, description, http_response_code, http_response_string, json_data):
        self.code = code
        self.description = description
        self.http_response_code = http_response_code
        self.http_response_string = http_response_string
        self.json_data = json_data

class DateTimeEncoder(JSONEncoder):

    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def register_agent(ws_config, device_name, agent_type, agent_version, agent_index, process_id):

    try:        
        jsonPostData = {"deviceName":device_name, "agentType":agent_type, "agentVersion":agent_version, "agentIndex":agent_index, "processID":process_id}

        method = "POST"
        path = 'v1/agent'
        url = ws_config.base_url + path
        headers = {"Content-Type": "application/json"}
        parameters = ''
        body = json.dumps(jsonPostData)
        
        response_code, response_string = CommonFunctions.send_signed_request(ws_config, method, url, path, headers, parameters, body)

    except Exception as ex:
        
        filename, line_number = CommonFunctions.get_exception_info()
        if filename is not None and line_number is not None:
            print(f"Exception occurred at line {line_number} in {filename}")
        print(ex)

        response_code = -1
        response_string = "Exception in RegisterAgent"

    return response_code, response_string
