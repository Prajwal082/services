import os

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

        load_dotenv()

        self.__init_logicApp_client()

    def __init_logicApp_client(self):

        subscription_id = os.environ['SUBSCRIPTION_ID']

        credential = Azidentity().authenticate()

        self.__lga_client = LogicManagementClient(
            credential = credential,
            subscription_id = subscription_id
        )

    
    def list_lgabyResuource_group(self,resource_group_name:str) -> List[str]:
        return [wflow.name for wflow in self.__lga_client.workflows.list_by_resource_group(resource_group_name = resource_group_name)]


    def run_trigger(self,reqbody:Dict[str, str]):
        
        self.__lga_client.workflow_triggers.run(
            resource_group_name = 'prajwal-rgp',
            workflow_name = 'lga-datastore',
            trigger_name = 'email_request',
            json = reqbody
        )

        # print([item.name for item in self.__lga_client.workflow_triggers.list(resource_group_name = 'prajwal-rgp',workflow_name='lga-datastore')])


    def send_email(
        self,
        to:List[str],
        cc:list[str],
        subject : str,
        body:str
    ) -> None:
    
        trigger_params = {
            "to"        : to,
            "cc"        : cc,
            "subject"   : subject,
            "body"      : body 
        }

        self.run_trigger(
            reqbody = trigger_params
        )

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pipeline_resp = args[0]
        if isinstance(pipeline_resp, PipelineResponse):
            self.logger.info('response handler: %s', pipeline_resp.http_response)

if __name__ == '__main__' : 

    obj = LogicApp()

    _to = 'pprajwal312@gmail.com'
    _cc = 'pprajwal312@gmail.com'
    _subject = 'Test email from Logic App!'
    _body = 'Hello, Good day!'

    obj.send_email(
        to=_to,
        cc=_cc,
        subject=_subject,
        body=_body
    )