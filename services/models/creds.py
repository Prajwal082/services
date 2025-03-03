from dataclasses import dataclass

@dataclass(frozen=True)
class AzSPNcreds:
    tenant_id: str
    client_id: str
    client_secret: str   


@dataclass(frozen=True)
class LogicAppConfig:
    subscription_id : str
    resource_group : str
    logicapp_name : str 
    logicapp_trigger : str