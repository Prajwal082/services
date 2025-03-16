import logging

import pandas as pd

from typing import *

from azure.storage.blob import (
    BlobServiceClient
)

from dotenv import load_dotenv

from services.identity.azidentity import Azidentity

from services.models.creds import AzSPNcreds

class BlobSvc():

    def __init__(self,storage_accountname:str,spn_cred_cntx:AzSPNcreds = None) -> None:

        load_dotenv()

        self.storage_accountname = storage_accountname
        self.spn_cred_cntx = spn_cred_cntx

        logging.basicConfig(level=logging.INFO)

        self.logger = logging.getLogger(__class__.__name__)

        self.__initBlobSvcClient()

    def __initBlobSvcClient(self):

        if self.spn_cred_cntx is not None:
            self.__credential = Azidentity().authenticate()
        else:
            az_creds = Azidentity(self.spn_cred_cntx)

            self.__credential = az_creds.authenticate()

        self.__blob_client = BlobServiceClient(
            account_url = f'https://{self.storage_accountname}.blob.core.windows.net',
            credential = self.__credential
        )


    def list_blobs(self,container_name:str,name_starts_with:str) -> DataFrame:
        container_client = self.__blob_client.get_container_client(container_name)

        blob_lst = container_client.list_blobs(name_starts_with = name_starts_with)

        columns = ['name','container','last_modified']
        data = []

        for blob in blob_lst:
            data.append([blob.get('name'),blob.get('container'),blob.get('last_modified')])

        return pd.DataFrame(data,columns=columns)
