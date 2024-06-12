import json

import ActionStreamer
from ActionStreamer import CommonFunctions
from ActionStreamer.WebService.API import WebServiceResult
from ActionStreamer.WebService.Patch import *

def create_video_clip(ws_config, device_name, video_clip):

    try:
        method = "POST"
        path = 'v1/videoclip/' + device_name
        url = ws_config.base_url + path
        headers = {"Content-Type": "application/json"}
        parameters = ''
        body = json.dumps(video_clip.__dict__)

        response_code, response_string = CommonFunctions.send_signed_request(ws_config, method, url, path, headers, parameters, body)

    except Exception as ex:
        
        filename, line_number = CommonFunctions.get_exception_info()
        if filename is not None and line_number is not None:
            print(f"Exception occurred at line {line_number} in {filename}")
        print(ex)

        response_code = -1
        response_string = "Exception in CreateVideoClip"

    return response_code, response_string


def update_file_id(ws_config, video_clip_id, file_id):

    try:
        operations_list = []
        add_patch_operation(operations_list, "FileID", file_id)

        method = "PATCH"
        path = 'v1/videoclip/' + video_clip_id
        url = ws_config.base_url + path
        headers = {"Content-Type": "application/json"}
        parameters = ''
        body = generate_patch_json(operations_list)

        response_code, response_code = CommonFunctions.send_signed_request(ws_config, method, url, path, headers, parameters, body)

    except Exception as ex:
        
        filename, line_number = CommonFunctions.get_exception_info()
        if filename is not None and line_number is not None:
            print(f"Exception occurred at line {line_number} in {filename}")
        print(ex)

        response_code = -1
        response_code = "Exception in UpdateVideoClipFileID"

    return response_code, response_code


class VideoClipClass:

    def __init__(self, file_id=0, ts_file_id=0, video_clip_parameters='', local_file_path='', height=0, width=0, frames_per_second=0, audio_status=0, start_time=0, start_time_ms=0, end_time=0, end_time_ms=0, clip_length_in_seconds=0):
        self.file_id = file_id
        self.ts_file_id = ts_file_id
        self.video_clip_parameters = video_clip_parameters
        self.local_file_path = local_file_path
        self.height = height
        self.width = width
        self.frames_per_second = frames_per_second
        self.audio_status = audio_status
        self.start_time = start_time
        self.start_time_ms = start_time_ms
        self.end_time = end_time
        self.EndTimeMS = end_time_ms
        self.ClipLengthInSeconds = clip_length_in_seconds

