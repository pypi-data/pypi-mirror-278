import re

# ----------------------------------------------------------
# HTTP definitions
# ----------------------------------------------------------

STATUS_OK = 200
STATUS_AUTH = 403

CONTENT_TYPE = 'Content-Type'
USER_AGENT = "User-Agent"

TEXT_PLAIN = 'text/plain'
APPLICATION_JSON = 'application/json'

ALL_TEXT = {TEXT_PLAIN}
ALL_JSON = {APPLICATION_JSON}
PATTERNS = {
    APPLICATION_JSON: [APPLICATION_JSON],
    TEXT_PLAIN: [TEXT_PLAIN],
}
# ----------------------------------------------------------
# Helpers
# ----------------------------------------------------------


def guess_content_type(headers):
    # TODO: 'application/json; charset=utf-8'
    # return APPLICATION_JSON
    content_type = headers.get(CONTENT_TYPE, TEXT_PLAIN).lower()

    for type_, patterns in PATTERNS.items():
        for pattern in patterns:
            if re.match(pattern, content_type):
                return type_

    #  fallback
    return APPLICATION_JSON
