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
            self.__spncred_cntx = self.__build_credentials()

    def __build_credentials(self):
        return AzSPNcreds(
                client_id     = os.environ['CLIENT_ID'],
                tenant_id     = os.environ['TENANT_ID'],
                client_secret = os.environ['SECRET']
        )

    def authenticate(self):
        try:
            if not isinstance(self.__spncred_cntx,AzSPNcreds):
                raise CredentialUnavailableError(
                    f'Credential passed is not of tyoe AzSPNcreds {type(self.__spncred_cntx)}'
                )

            self._credential = ClientSecretCredential(**asdict(self.__spncred_cntx))

            return self._credential

        except Exception as err:
            self.logger.error(err)
            raise err

    def get_access_token(self,scope:str) -> Dict:
        return self._credential.get_token(scope)
        
