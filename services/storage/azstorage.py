import logging
import pprint

from azure.storage.blob import (
    BlobServiceClient,
    ContainerClient
)

from dotenv import load_dotenv

from services.identity.azidentity import Azidentity

from services.models.creds import AzSPNcreds

from collections import defaultdict


class BlobSvc():

    def __init__(self,storage_accountname:str,spn_cred_cntx:AzSPNcreds = None) -> None:

        load_dotenv()

        self.storage_accountname = storage_accountname
        self.spn_cred_cntx = spn_cred_cntx

        logging.basicConfig(level=logging.INFO)

        self.logger = logging.getLogger(__class__.__name__)

        self.__initBlobSvcClient()

        self.__default_dict = defaultdict()

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


    def list_blobs(self,container_name:str,path:str) :
        container_client = self.__blob_client.get_container_client(container_name)

        blob_lst = container_client.list_blobs(name_starts_with = 'iceberg_catalog/IcebergDB/checkpoint/')

        key_info = ['name','container','last_modified']

        for blob in blob_lst:

            self.__default_dict[key_info[0]] = blob.get(key_info[0])
            self.__default_dict[key_info[1]] = blob.get(key_info[1])
            self.__default_dict[key_info[2]] = blob.get(key_info[2])

        return self.__default_dict

obj = BlobSvc('poctrials')

pprint.pprint(obj.list_blobs('raw'))
