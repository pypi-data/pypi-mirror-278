import json

import ActionStreamer
from ActionStreamer import CommonFunctions
from ActionStreamer.WebService.API import WebServiceResult

def get_pending_event_list(ws_config, device_name):

    ws_result = WebServiceResult(0, '', '', '', None)

    try:
        method = "POST"
        path = 'v1/event/list/pending'
        url = ws_config.base_url + path
        headers = {"Content-Type": "application/json"}
        parameters = ''

        json_post_data = {
            "deviceName": device_name
        }

        body = json.dumps(json_post_data)
        
        response_code, response_string = CommonFunctions.send_signed_request(ws_config, method, url, path, headers, parameters, body)
        
        ws_result.http_response_code = response_code
        ws_result.http_response_string = response_string
        ws_result.json_data = json.loads(response_string)

    except Exception as ex:
        ws_result.code = -1
        filename, line_number = CommonFunctions.get_exception_info()
        if filename is not None and line_number is not None:
            print(f"Exception occurred at line {line_number} in {filename}")
        print(ex)

    return ws_result 


def dequeue_event(ws_config, device_name, agent_type):

    ws_result = WebServiceResult(0, '', '', '', None)

    try:
        method = "POST"
        path = 'v1/event/dequeue'
        url = ws_config.base_url + path
        headers = {"Content-Type": "application/json"}
        parameters = ''

        json_post_data = {
            "deviceName": device_name,
            "agentType": agent_type
        }

        body = json.dumps(json_post_data)
        
        response_code, response_string = CommonFunctions.send_signed_request(ws_config, method, url, path, headers, parameters, body)
        
        ws_result.http_response_code = response_code
        ws_result.http_response_string = response_string
        ws_result.json_data = json.loads(response_string)

    except Exception as ex:
        ws_result.code = -1
        filename, line_number = CommonFunctions.get_exception_info()
        if filename is not None and line_number is not None:
            print(f"Exception occurred at line {line_number} in {filename}")
        print(ex)

    return ws_result 


def create_event(ws_config, device_name, agent_type, event_type, event_parameters, priority=1, max_attempts=0, expiration_date=None):

    ws_result = WebServiceResult(0, '', '', '', None)

    try:
        method = "POST"
        path = 'v1/event'
        url = ws_config.base_url + path
        headers = {"Content-Type": "application/json"}
        parameters = ''

        json_post_data = {
            "deviceName": device_name,
            "agentType": agent_type,
            "eventType": event_type,
            "eventParameters": event_parameters,
            "priority": priority,
            "maxAttempts": max_attempts,
            "expirationDate": expiration_date
        }

        body = json.dumps(json_post_data)
        
        response_code, response_string = CommonFunctions.send_signed_request(ws_config, method, url, path, headers, parameters, body)
        
        ws_result.http_response_code = response_code
        ws_result.http_response_string = response_string
        ws_result.json_data = json.loads(response_string)

    except Exception as ex:
        ws_result.code = -1
        filename, line_number = CommonFunctions.get_exception_info()
        if filename is not None and line_number is not None:
            print(f"Exception occurred at line {line_number} in {filename}")
        print(ex)

    return ws_result


def get_event_details(ws_config, event_id):

    ws_result = WebServiceResult(0, '', '', '', None)

    try:
        method = "GET"
        path = 'v1/event/' + event_id
        url = ws_config.base_url + path
        parameters = ''
        headers = {}
        body = ''
        
        response_code, response_string = CommonFunctions.send_signed_request(ws_config, method, url, path, headers, parameters, body)
        
        ws_result.http_response_code = response_code
        ws_result.http_response_string = response_string
        ws_result.json_data = json.loads(response_string)

    except Exception as ex:
        ws_result.code = -1
        filename, line_number = CommonFunctions.get_exception_info()
        if filename is not None and line_number is not None:
            print(f"Exception occurred at line {line_number} in {filename}")
        print(ex)

    return ws_result 


def update_event(ws_config, event_id, event_status, result, tag_string='', tag_number=0, attempt_number=1):

    ws_result = WebServiceResult(0, '', '', '', None)

    try:
        method = "PUT"
        path = 'v1/event' + event_id
        url = ws_config.base_url + path
        headers = {"Content-Type": "application/json"}
        parameters = ''

        json_post_data = {
            "eventStatus": event_status,
            "attemptNumber": attempt_number,
            "result": result,
            "tagString": tag_string,
            "tagNumber": tag_number
        }

        body = json.dumps(json_post_data)
        
        response_code, response_string = CommonFunctions.send_signed_request(ws_config, method, url, path, headers, parameters, body)
        
        ws_result.http_response_code = response_code
        ws_result.http_response_string = response_string
        ws_result.json_data = json.loads(response_string)

    except Exception as ex:
        ws_result.code = -1
        filename, line_number = CommonFunctions.get_exception_info()
        if filename is not None and line_number is not None:
            print(f"Exception occurred at line {line_number} in {filename}")
        print(ex)

    return ws_result