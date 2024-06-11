from nomad_media_pip.src.admin.live_input.get_live_input import _get_live_input

def _get_live_input_status_message(self, AUTH_TOKEN, URL, INPUT_ID, DEBUG):
    # Get the live input
    INPUT = _get_live_input(self, AUTH_TOKEN, URL, INPUT_ID, DEBUG)

    # Check if input was found
    if (INPUT):
        # Check if there is status message
        if (INPUT["statusMessage"] and INPUT["statusMessage"]):
            # Return input status message
            return INPUT["statusMessage"]

    # There is no status message
    return ""

