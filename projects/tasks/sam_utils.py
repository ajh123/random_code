from typing import Type, List

def validated_input(res_type: Type, message: str, invalid_message: str):
    '''
    A generic function to validate an input based on a data type.

    This function will catch all ValueErrors thrown by the data types constructor

    @param res_type: Any constructor for any data type, the constructor must take one paramater.
    @param message: The message to diaplay to the user when they input.
    @param invalid_message: The message to display when the user inputs an invalid data type.
    '''
    ok = False # Variable used to check if the data input is valid
    res = None # The result returned from the function
    while not ok: # Trap the user in a loop until a valid data type is given
        try: # Check for any errors
            # Retreieve input from the user (and display the message), then cast the result to the given data type.
            # If casting is unsuccessfull a ValueError would be thrown
            res = res_type(input(message))
            ok = True # If the program gets here it means that no ValueErrors were thrown, so we can assume the casting was ok
        except ValueError:
            print(invalid_message) # If there were a value error display the user a message
    return res

def validate_list_input(list: List[str], message: str, invalid_message: str) -> str:
    '''
    A generic function to validate an input based on values in a string list.

    This function will check if the users input is contained in the list and waits until the user enters a valid list value.

    The function will return the user's input.

    @param list: The list you wish to compare againist.
    @param message: The message to diaplay to the user when they input.
    @param invalid_message: The message to display when the user inputs an object thats not in the list.
    '''

    ok = False # Variable used to check if the data input is valid
    res = None # The result returned from the function
    while not ok:
        res = input(message)
        if res in list: # Check if the input is in the list
            ok = True
        else:
            print(invalid_message) # otherwise display an error message

    return res

def display_list(list: List[str]) -> str:
    out = ""
    for ele in list:
        out += f"{ele}, "
    return out