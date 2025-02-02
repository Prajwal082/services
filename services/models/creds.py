from dataclasses import dataclass

@dataclass(frozen=True)
class AzSPNcreds:
    tenant_id: str
    client_id: str
    client_secret: str   

class LogicApp:
    ... 

class LogicAppConfig:
    spn_creds : AzSPNcreds
    subscription_id : str