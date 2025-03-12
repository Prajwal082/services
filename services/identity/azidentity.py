import logging 
import os

from typing import Any, List, Dict

from dotenv import load_dotenv

from dataclasses import asdict

from azure.identity import (
    ClientSecretCredential,
    CredentialUnavailableError
)

from services.models.creds import AzSPNcreds

from azure.keyvault.secrets import SecretClient 


class Azidentity:

    def __init__(self,spn_cred_cntx:AzSPNcreds = None) -> None:

        self.logger = logging.getLogger(__class__.__name__)

        self.__spncred_cntx = spn_cred_cntx
        
        if not self.__spncred_cntx:
            load_dotenv()
            self.__spncred_cntx = self.__build__credentials()

        self.__authenticate()

    def __build__credentials(self):
        return AzSPNcreds(
                client_id     = os.environ['CLIENT_ID'],
                tenant_id     = os.environ['TENANT_ID'],
                client_secret = os.environ['SECRET']
        )

    def __authenticate(self):
        try:
            if not isinstance(self.__spncred_cntx,AzSPNcreds):
                raise CredentialUnavailableError(
                    f'Credential passed is not of tyoe AzSPNcreds {type(self.__spncred_cntx)}'
                )

            self.__credential = ClientSecretCredential(**asdict(self.__spncred_cntx))

            return self.__credential

        except Exception as err:
            self.logger.error(err)
            raise err

    def get_access_token(self,scope:str) -> Dict:
        '''Get Token from AAD for the scope'''
        return self.__credential.get_token(scope)
    
    def list_secrets(self,vault_url:str) -> List[List]:
        '''Lists all the secrets in the Key Vault with name and last updated'''
        secret_list = []
        sc =  SecretClient(vault_url=vault_url,credential=self.__credential)
        for _sc in sc.list_properties_of_secrets():
            secret_list.append([_sc.name,_sc.updated_on])
        return secret_list
    
    def get_secret(self,vault_url:str,secret_name:str) -> str:
        '''Fetch the secret value from AKV'''
        sc =  SecretClient(vault_url=vault_url,credential=self.__credential)

        return sc.get_secret(name=secret_name).value
        
