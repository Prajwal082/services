import os

import logging

from typing import Any,List,Dict

from dotenv import load_dotenv

from services.identity.azidentity import Azidentity

from azure.core.pipeline import PipelineResponse

from services.models.creds import ( 
    AzSPNcreds,
    LogicAppConfig)


from azure.mgmt.logic import LogicManagementClient

class LogicApp:

    def __init__(self,lga_config=None):

        self.logger = logging.getLogger(__class__.__name__)

        load_dotenv()

        self.lga_config = LogicAppConfig(
            subscription_id  = os.environ['SUBSCRIPTION_ID'],
            resource_group   = os.environ['RESOURCE_GROUP_NAME'],
            logicapp_name    = os.environ['LOGIC_APP_NAME'],
            logicapp_trigger = os.environ['LOGIC_APP_TRIGGER']
        )

        self.__init_logicApp_client()

    def __init_logicApp_client(self):

        credential = Azidentity().authenticate()

        self.__lga_client = LogicManagementClient(
            credential = credential,
            subscription_id = self.lga_config.subscription_id
        )

    
    def list_lgabyResuource_group(self,resource_group_name:str) -> List[str]:
        return [wflow.name for wflow in self.__lga_client.workflows.list_by_resource_group(resource_group_name = resource_group_name)]


    def run_trigger(self,reqbody:Dict[str, str]):
        
        self.__lga_client.workflow_triggers.run(
            resource_group_name = self.lga_config.resource_group,
            workflow_name = self.lga_config.logicapp_name,
            trigger_name = self.lga_config.logicapp_trigger,
            json = reqbody
        )

    def send_email(
        self,
        to:List[str],
        cc:list[str],
        subject : str,
        body:str
    ) -> None:

        assert to is not None and subject is not None and body is not None, "Empty params are not supported!"
    
        trigger_params = {
            "to"        : to,
            "cc"        : cc,
            "subject"   : subject,
            "body"      : body 
        }

        self.logger.info("Email Trigger with params :%s",trigger_params)

        self.run_trigger(
            reqbody = trigger_params
        )
        