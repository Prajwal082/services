import logging
import os

from typing import *

from services.identity.azidentity import Azidentity

from azure.storage.blob import (
    BlobServiceClient,
    ContainerClient
)

from dotenv import load_dotenv

class StorageSVC:

    def __init__(self) -> None:

        load_dotenv()

        logging.basicConfig(
            level=logging.INFO,
            format=f'[%(asctime)s]:[%(levelname)s]:[%(name)s:%(lineno)-2s] %(message)s'
        )

        self.logger = logging.getLogger(__class__.__name__)

        self.logger.info("Initializing Blob Service client..")

        self.__initblobserviceclient()

    def __initblobserviceclient(self):

        credential = Azidentity.authenticate()

        self.blob_client = BlobServiceClient(
            account_url= os.environ['STORAGE_ACCOUNT_URL'],
            credential=credential
        )

    def list_blob(self):
        ...

    def download_blob(self):
        ... 

    def upload_blob(self):
        ...


if __name__ == '__main__':

    obj = StorageSVC()
