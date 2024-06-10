# keyvault.py

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import requests


############
# CLASS DEFS

class KeyVaultError(Exception):
    '''
    Exception raised when program fails to connect to and pull data from
    an Azure secrets vault
    '''
    def __init__(self, orig_err):
        self.orig_err = orig_err
        self.message = ('error connecting to and pulling data from Azure '
                        'secrets vault')
        super().__init__(self.message)


#########
# FN DEFS

def get_vault_name(dotenv_filename):
    '''
    get an Azure secrets vault name from the given dotenv file
    '''
    vault_name = get_dotenv_vals(dotenv_filename, ['VAULT_NAME'])
    return vault_name


def get_secret(vault_name, secret_name):
    '''
    get the given secrets from the given Azure secrets vault
    '''
    credential = DefaultAzureCredential()
    vault_url = f'https://{vault_name}.vault.azure.net'
    client = SecretClient(vault_url=vault_url,
                          credential=credential,
                         )
    # get requested secrets
    try:
        secret = client.get_secret(secret_name).value
    # or log authentication/connection/etc error
    except Exception as e:
        raise SecretsVaultError(e)
    return secret

