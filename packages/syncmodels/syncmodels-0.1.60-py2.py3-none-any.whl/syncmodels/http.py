import re

# ----------------------------------------------------------
# HTTP definitions
# ----------------------------------------------------------

STATUS_OK = 200
STATUS_AUTH = 403

CONTENT_TYPE = 'Content-Type'
USER_AGENT = "User-Agent"
AUTHORIZATION = "Authorization"

TEXT_PLAIN = 'text/plain'
APPLICATION_JSON = 'application/json'
APPLICATION_XML = 'application/xml'

ALL_TEXT = {TEXT_PLAIN}
ALL_JSON = {APPLICATION_JSON}
ALL_XML = {APPLICATION_XML}
PATTERNS = {
    APPLICATION_JSON: [APPLICATION_JSON],
    TEXT_PLAIN: [TEXT_PLAIN],
    APPLICATION_XML: [APPLICATION_XML],
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


async def extract_result(response):
    content_type = guess_content_type(response.headers)
    if content_type in ALL_JSON:
        result = await response.json()
    elif content_type in ALL_XML:
        result = await response.text()
    else:
        result = await response.text()

    return result
