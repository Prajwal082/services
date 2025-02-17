import logging

from typing import *

from services.identity.azidentity import Azidentity

from azure.storage.blob import (
    BlobServiceClient,
    ContainerClient
)

class StorageSVC:

    def __init__(self) -> None:
        self.logger = logging.getlogger(__class__.__name__)

        self.logger("Helloe")

