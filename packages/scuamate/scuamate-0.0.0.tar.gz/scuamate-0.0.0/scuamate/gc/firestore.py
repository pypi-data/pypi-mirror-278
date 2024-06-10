# firestore.py

import json
from firebase_admin import credentials, initialize_app, firestore

from scuamate import get_dotenv_vals
from scuamate.az.kevault import get_secret


def get_access_info(dotenv_filename,
                    dburl_dotenv_val,
                    secretname_dotenv_val,
                    azure_vault_name,
                   ):
    '''
    read the Firestore database URL ('dburl_dotenv_val')
    and the Azure KeyVault secret name ('secretname_dotenv_val')
    from the given dotenv-file ('dotenv_filename'),
    get the password from the given Azure KeyVault ('azure_vault_name'),
    then use all of that info to retrieve and return the information
    needed for access to the Firestore database
    (the Firebase access key and the database URL)
    '''
    key_name, db_url = get_dotenv_vals(dotenv_filename,
                                       [secretname_dotenv_val,
                                        dburl_dotenv_val,
                                       ],
                                      )
    key = get_secret(vault_name, key)
    # prep connection info
    acc_info = {'firebaseKey' : json_key,
                'databaseURL': db_url,
               }
    return acc_info


def get_cert(key):
    '''
    use the given key (either a dict of JSON-derived content or
    a string representation of that that can be parsed by json.loads)
    to create and return a firebase_admin.credentials.Certificate object
    '''
    if not isinstance(key, dict):
        key = json.loads(key)
    cert = credentials.Certificate(key)
    return cert


def connect_to_db(acc_info):
    '''
    use the given dict of access info (including a 'firebaseKey':<KEY> pair
    and a 'databaseURL': <URL> pair) to certify, initialize an app,
    and connect to the database,
    returning both the app and database-client objects
    '''
    cert = get_cert(acc_info.pop('firebaseKey'))
    app = firebase_admin.initialize_app(cert, acc_info)
    db = firestore.client()
    return (app, db)

