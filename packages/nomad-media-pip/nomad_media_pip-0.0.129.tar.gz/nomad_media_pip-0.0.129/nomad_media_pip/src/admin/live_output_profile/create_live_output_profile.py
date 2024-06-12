from nomad_media_pip.src.helpers.send_request import _send_request

import requests, json, time
MAX_RETRIES = 2

def _create_live_output_profile(self, AUTH_TOKEN, URL, NAME, OUTPUT_TYPE, ENABLED, AUDIO_BITRATE,
                        OUTPUT_STREAM_KEY, OUTPUT_URL, SECONDARY_OUTPUT_STREAM_KEY,
                        SECONDARY_OUTPUT_URL, VIDEO_BITRATE, VIDEO_BITRATE_MODE,
                        VIDEO_CODEC, VIDEO_FRAMES_PER_SECOND, VIDEO_HEIGHT, VIDEO_WIDTH,
                        DEBUG):

    API_URL = f"{URL}/api/liveOutputProfile"

    BODY = {
        "name": NAME,
        "outputType": OUTPUT_TYPE,
        "enabled": ENABLED,
        "audioBitrate": AUDIO_BITRATE,
        "outputStreamKey": OUTPUT_STREAM_KEY,
        "outputUrl": OUTPUT_URL,
        "secondaryOutputStreamKey": SECONDARY_OUTPUT_STREAM_KEY,
        "secondaryOutputUrl": SECONDARY_OUTPUT_URL,
        "videoBitrate": VIDEO_BITRATE,
        "videoBitrateMode": VIDEO_BITRATE_MODE,
        "videoCodec": VIDEO_CODEC,
        "videoFramesPerSecond": VIDEO_FRAMES_PER_SECOND,
        "videoHeight": VIDEO_HEIGHT,
        "videoWidth": VIDEO_WIDTH
    }

    return _send_request(self, AUTH_TOKEN, "Create live output profile", API_URL, "POST", None, BODY, DEBUG)