# azfuncs.py

from azure.functions import HttpResponse


def make_httpresponse(successful, message=None):
    '''
    return an Azure function HTTP Response based on whether or not
    a given operation was successful
    '''
    statuses = {True: 200,
                False: 500,
               }
    status = statuses[successful]
    response = HttpResponse(body=message,
                            status_code=status,
                           )
    return response

