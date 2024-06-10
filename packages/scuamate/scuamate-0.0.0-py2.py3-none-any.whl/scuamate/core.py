# core.py

import numpy as np
import logging
import re
import os
from datetime import datetime, timedelta
from dotenv import dotenv_values
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import requests


############
# CLASS DEFS

class GetRequestError(Exception):
    '''
    Exception raised when a GET request has a non-200 status
    '''
    def __init__(self, orig_err, status_code):
        self.orig_err = orig_err
        self.message = f'GET request response status code ({status_code}) not ok'
        self.status_code = status_code
        if status_code == 429:
            self.message += ('\n(Too Many Requests; '
                             'if using API, probably hit rate limit')
        super().__init__(self.message)


class InvalidPointsError(ValueError):
    '''
    Exception raised when a value fails to be converted to a
    `gpd.GeoDataFrame` of points
    '''
    def __init__(self, data_source, orig_err):
        self.data_source = data_source
        self.orig_err = orig_err
        message = (f'positions data returned from {self.data_source} could '
                   f'not be coerced to a `gpd.GeoDataFrame` of points')
        self.messageg = message
        super().__init__(self.message)





#########
# FN DEFS

def make_sample_env_file(dotenv_filename,
                         out_sample_dotenv_filename=None,
                         overwrite=False,
                        ):
    '''
    simple utility for running locally, to create a sample.env file
    by reading the given .env file (dotenv_filename)
    and removing and replacing all sensitive values
    '''
    if out_sample_dotenv_filename is None:
        out_sample_dotenv_filename = 'sample' + dotenv_filename
    with open(dotenv_filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    newlines = [re.sub("(?<==').*(?=')",
                       f"<{re.search('^[A-Z_-]+(?==)', line).group()}>",
                       line) for line in lines]
    assert not os.path.isfile(out_sample_dotenv_filename) or overwrite, ('cannot '
        "overwrite existing file unless 'overwrite' arg == True!")
    with open(out_sample_dotenv_filename, 'w') as f:
        f.write('\n'.join(newlines)+'\n')
    print(f"\n\n'{out_sample_dotenv_filename}' written\n\n")


def get_logging_configs(local_pathstr=None):
    '''
    simple function to return a dict of **kwargs for `logging.basicConfig`,
    to ensure that all logging calls happen from the `main()` function
    associated with a given task
    '''
    format='%(levelname)s: %(asctime)s: %(message)s'
    # if on my local machine, set logging level to DEBUG,
    # filemode to write,
    # and format to indicate I'm manually running the code
    if local_pathstr is not None and local_pathstr in os.getcwd():
        level = 'INFO'
        filemode = 'w'
        format = 'MANUAL RUN: ' + format
    # otherwise, set to appropriate configs for production use
    else:
        level = 'INFO'
        filemode='a'
    configs = {'format': format,
               'level': level,
               'filemode': filemode,
              }
    return configs


def get_dotenv_vals(dotenv_filename, keys_list):
    '''
    query a dotenv config file for the values corresponding to the list of keys;
    returns a single val (if just 1 requested) or a list of vals (if >1)
    '''
    # grab all info from the .env config file
    config = dotenv_values(dotenv_filename)
    # extract and return requested vals
    vals = [config[key] for key  in keys_list]
    # same number of keys as vals?
    assert len(vals) == len(keys_list)
    # all strings?
    assert np.all([isinstance(val, str) for val in vals])
    if len(vals) == 1:
        val = vals[0]
        return val
    else:
        return vals


def get_prev_utc_datetime(**kwargs):
    '''
    get a datetime object for the indicated time ago
    (using kwargs fed to `datetime.datetime.timedelta`)
    '''
    time_ago = (datetime.utcnow() - timedelta(**kwargs))
    return time_ago


def get_request(request_url, **kwargs):
    '''
    run a `requests.get` call, check the status of the response, then return it;
    **kwargs get passed through to `requests.get`
    '''
    response = requests.get(request_url, **kwargs)
    try:
        assert response.status_code == requests.codes.ok
    except Exception as e:
        raise GetRequestError(e, response.status_code)
    return response

