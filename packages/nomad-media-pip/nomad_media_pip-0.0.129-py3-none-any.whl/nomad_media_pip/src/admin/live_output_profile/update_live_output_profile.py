from nomad_media_pip.src.helpers.send_request import _send_request
from nomad_media_pip.src.admin.live_output_profile.get_live_output_profile import _get_live_output_profile

def _update_live_output_profile(self, AUTH_TOKEN, URL, ID, NAME, OUTPUT_TYPE, ENABLED, AUDIO_BITRATE,
                        OUTPUT_STREAM_KEY, OUTPUT_URL, SECONDARY_OUTPUT_STREAM_KEY,
                        SECONDARY_OUTPUT_URL, VIDEO_BITRATE, VIDEO_BITRATE_MODE,
                        VIDEO_CODEC, VIDEO_FRAMES_PER_SECOND, VIDEO_HEIGHT, VIDEO_WIDTH,
                        DEBUG):

    API_URL = f"{URL}/api/liveOutputProfile"

    PROFILE_INFO = _get_live_output_profile(self, AUTH_TOKEN, URL, ID, DEBUG)

    BODY = {
        "id": ID,
        "name": NAME or PROFILE_INFO.get("name"),
        "outputType": OUTPUT_TYPE or PROFILE_INFO.get("outputType"),
        "enabled": ENABLED or PROFILE_INFO.get("enabled"),
        "audioBitrate": AUDIO_BITRATE or PROFILE_INFO.get("audioBitrate"),
        "outputStreamKey": OUTPUT_STREAM_KEY or PROFILE_INFO.get("outputStreamKey"),
        "outputUrl": OUTPUT_URL or PROFILE_INFO.get("outputUrl"),
        "secondaryOutputStreamKey": SECONDARY_OUTPUT_STREAM_KEY or PROFILE_INFO.get("secondaryOutputStreamKey"),
        "secondaryOutputUrl": SECONDARY_OUTPUT_URL or PROFILE_INFO.get("secondaryOutputUrl"),
        "videoBitrate": VIDEO_BITRATE or PROFILE_INFO.get("videoBitrate"),
        "videoBitrateMode": VIDEO_BITRATE_MODE or PROFILE_INFO.get("videoBitrateMode"),
        "videoCodec": VIDEO_CODEC or PROFILE_INFO.get("videoCodec"),
        "videoFramesPerSecond": VIDEO_FRAMES_PER_SECOND or PROFILE_INFO.get("videoFramesPerSecond"),
        "videoHeight": VIDEO_HEIGHT or PROFILE_INFO.get("videoHeight"),
        "videoWidth": VIDEO_WIDTH or PROFILE_INFO.get("videoWidth")
    }

    return _send_request(self, AUTH_TOKEN, "Update live output profile", API_URL, "PUT", None, BODY, DEBUG)