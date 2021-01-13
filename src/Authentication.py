import re


"""
Regex string of the format used to validate credentials
"""
credential_format = "[0-9][a-zA-Z]{3}[0-9]{3}"


"""
Allows creator/owner of API to change format of authentication of credentials
Inputs: String API_key (to ensure owner currently has valid authentication credentials), String format (the updated credential format)
"""
def set_credential_format(API_Key, format):
    global credential_format
    if (validate_credentials(API_key)):
        credential_format = format
    return


"""
Validates a given set of credentials
Input: credentials (string)
Output: True if valid
"""
def validate_credentials(API_key):
    global credential_format

    return re.match(credential_format, API_key)

    
    

    