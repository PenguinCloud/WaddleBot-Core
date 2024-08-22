from dataclasses import dataclass

@dataclass
class messageData():
    text: str
    channel: str
    username: str
    userid: str
    avatar: str
    account: str
    event: str
    protocol: str
    gateway: str
    parent_id: str
    timestamp: str
    id: str
    Extra: str

@dataclass
class marketplaceModuleData():
    name: str
    description: str
    gateway_url: str
    module_type_id: int
    metadata: dict

@dataclass
class commandData():
    action: str
    description: str
    method: str
    parameters: list
    payload_keys: list

@dataclass
class sendMessageData():
    text: str
    username: str
    gateway: str
    account: str

@dataclass
class identityData():
    identity_name: str

