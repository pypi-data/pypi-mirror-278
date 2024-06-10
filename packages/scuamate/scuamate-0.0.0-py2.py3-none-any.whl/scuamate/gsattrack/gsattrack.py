# gsattrack.py

import requests
from datetime import datetime
import pandas as pd
import geopandas as gpd
import csv
import logging
import os

from scuamate import (get_request,
                      get_prev_utc_datetime,
                      get_dotenv_vals,
                      InvalidPointsError,
                      KeyVaultError,
                      GetRequestError,
                     )
from scuamate.az.keyvault import get_secret

##########
# FN DEFS:

def format_datetime(datetime):
    '''
    format a Python datetime object to match
    the format expected by the GSatTrack API
    '''
    return datetime.isoformat()


def get_formatted_prev_utc_time(**kwargs):
    '''
    get a properly formatted timestamp for some amount of time ago
    (using kwargs fed to `datetime.datetime.timedelta`),
    '''
    dt = get_prev_utc_datetime(**kwargs)
    assert isinstance(dt, datetime)
    return format_datetime(dt)


def get_token(username, pwd):
    '''
    authenticate through the GSatTrack API and retrieve auth token
    '''
    request_url = 'https://www.gsattrack.com/api/token'
    headers = {'Accept': 'application/json',
               'Authorization': 'Basic',
              }
    response = get_request(request_url,
                           headers=headers,
                           auth=(username, pwd),
                          )
    return response.json()


def get_access_info(dotenv_filename,
                    username_dotenv_val,
                    accountname_dotenv_val,
                    secretname_dotenv_val,
                    azure_vault_name,
                   ):
    '''
    read the GSatTrack user name ('username_dotenv_val'),
    account name ('accountname_dotenv_val'),
    and Azure KeyVault secret name ('secretname_dotenv_val')
    from the given dotenv-file ('dotenv_filename'),
    get the password from the given Azure KeyVault ('azure_vault_name'),
    then use all of that info to retrieve and return the information
    needed for access to the GSatTrack API
    (the GSatTrack user name, account GUID, password, and JSON Web Token)
    '''
    (username,
     secret_name,
     guid) = get_dotenv_vals(dotenv_filename,
                             [username_dotenv_val,
                              secretname_dotenv_val,
                              accountname_dotenv_val,
                             ],
                            )
    try:
        pwd = get_secret(azure_vault_name, secret_name)
    except KeyVaultError as e:
        logging.critical(e.message)
    # authorize with GSatTrack to get JSON Web Token (JWT)
    try:
        jwt = get_token(username, pwd)
    except GetRequestError as e:
        logging.critical(e.message)
    acc_info = {'username': username,
                'accountname': guid,
                'password': pwd,
                'token': jwt,
               }
    return acc_info


def get_all_assets(gst_client_id, jwt):
    '''
    Get all assets (i.e., tags/'devices') from GSatTrack API
    NOTE: 'device' in our dataset's parlance is not the same as 'device'
          according to the GSatTrack API!
    '''
    # build API-request URL
    request_url = f"https://www.gsattrack.com/api/clients/{gst_client_id}/assets"
    headers = {'Authorization': f'Bearer {jwt}',
              }
    # get and parse response
    response = get_request(request_url,
                           headers=headers,
                          )
    assets_df = pd.DataFrame(response.json())
    assets_df = assets_df[['id',
                           'name',
                           'createdOnUtc',
                           'deviceId',
                           'color',
                           'iconType']]
    return assets_df


def get_points(jwt,
               gst_client_id,
               from_time,
               to_time,
               asset_id=None,
               assets_df=None,
               page_num=None,
               request_kwargs=None
              ):
    '''
    Use auth token (JWT) to get latest positons from GSatTrack.
    Can return all positions, or positions for a specific asset_id
    (NOTE: an 'asset', in GSatTrack parlance, is what we call a 'device',
    whereas GSatTrack uses 'device' differently!)
    '''
    if request_kwargs is None:
        request_kwargs = {}
    assert from_time is not None and to_time is not None, ('must provide '
                                                          'a from_time and '
                                                          'a to_time!')
    if asset_id is None:
        pass
    elif isinstance(asset_id, int):
        pass
    elif (isinstance(asset_id, str) and
          len(asset_id) == 9 and
          assets_df is not None):
        asset_id = assets_df[assets_df['name']==asset_id]['id'].values[0]
    else:
        raise ValueError(("if 'asset_id' is provided it must either be "
                          "an 'assetId' integer value, "
                          "as used by the GSatTrack API, "
                          "or else a 'device_id' 9-digit string, as used by "
                          "us and stored as the 'title' of each GSatTrack "
                          "location ping."))
    asset_id_str = f"{asset_id}/" * (asset_id is not None)
    # format the request URL 
    headers = {'Authorization': f'Bearer {jwt}', }
    request_url = ('https://www.gsattrack.com/api/clients/'
                   f'{gst_client_id}/'
                   f'positions/{asset_id_str}'
                   f'geojson?from={from_time}'
                   f'&to={to_time}')
    # either get the page number specified,
    # or else start on first page and loop through
    if page_num is not None:
        page_num_provided = True
    else:
        page_num_provided = False
        page_num = 1
    print(f'\t\tgetting page {page_num} of results...')
    response = get_request(request_url+f'&page={page_num}',
                           headers=headers,
                           **request_kwargs,
                          )
    page = response.json()['page']
    assert page == page_num
    # grab all the positions (i.e., spatial features)
    features = response.json()['features']
    if not page_num_provided:
        last_page = response.json()['pages']
        total = response.json()['total'] # total number of positions available
        while page < last_page:
            page_num += 1
            print(f'\t\tgetting page {page_num} of results...')
            response = get_request(request_url+f'&page={page_num}',
                                   headers=headers,
                                  )
            page = response.json()['page']
            assert page == page_num
            features.extend(response.json()['features'])
        assert len(features) == total
    # check data can be coerced to points gdf
    try:
        pts = gpd.GeoDataFrame.from_features(features)
    except Exception as e:
        raise InvalidPointsError('GSatTrack API', e)
    if len(pts) > 0:
        # coerce timestamps to pandas.Timestamp objects
        # NOTE: times expressed in UTC (which we know from the concatenated 'Z')
        pts['time'] = pts['time'].apply(lambda t_str:
                                                pd.Timestamp(t_str.rstrip('Z')))
        pts['received'] = pts['received'].apply(lambda t_str:
                                                pd.Timestamp(t_str.rstrip('Z')))
        # ensure that points are chronologically ordered
        pts = pts.sort_values('received')
        # ensure their CRS is set to unprojected lat-lon
        if pts.crs is None:
            pts = pts.set_crs(4326)
    return pts

