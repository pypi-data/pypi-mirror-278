import datetime
import json

import ActionStreamer
from ActionStreamer import CommonFunctions
from ActionStreamer.WebService.API import WebServiceResult

def create_log_message(log_config, message, log_to_console=True):

    try:
        if (log_to_console):
            CommonFunctions.Log(message, log_config.agentName)

        utc_now = datetime.datetime.now(datetime.timezone.utc)
        post_data = {"deviceSerial":log_config.device_name, "agentType":log_config.agent_type, "agentVersion":log_config.agent_version, "agentIndex":log_config.agent_index, "processID":log_config.process_id, "message":message, "logDate": utc_now}

        method = "POST"
        path = 'v1/logmessage'
        url = log_config.ws_config.base_url + path
        headers = {"Content-Type": "application/json"}
        parameters = ''
        body = json.dumps(post_data)

        response_code, response_string = CommonFunctions.send_signed_request(log_config.ws_config, method, url, path, headers, parameters, body)

    except Exception as ex:
        
        filename, line_number = CommonFunctions.get_exception_info()
        if filename is not None and line_number is not None:
            print(f"Exception occurred at line {line_number} in {filename}")
        print(ex)

        response_code = -1
        response_string = "Exception in CreateLogMessage"

    return response_code, response_string