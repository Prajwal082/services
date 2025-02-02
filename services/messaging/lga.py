import os

from typing import Any

from services.identity.azidentity import Azidentity

from services.models.creds import ( 
    AzSPNcreds,
    LogicAppConfig)


from azure.mgmt.logic import LogicManagementClient

class LogicApp:

    def __init__(self,lga_config=None):
        self.__init_logicApp_client()

    def __init_logicApp_client(self):

        credential = Azidentity().authenticate()

        self.__lga_client = LogicManagementClient(
            credential = credential,
            subscription_id = 'eaa1b6ae-9783-4570-8232-27c313188c9f'
        )


    def run_trigger(self):
        ...

        
if __name__ =='__main__':

    obj = LogicApp()