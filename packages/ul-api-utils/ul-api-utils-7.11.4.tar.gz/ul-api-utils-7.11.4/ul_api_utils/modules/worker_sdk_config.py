from pydantic import BaseModel, Extra

from ul_api_utils.resources.socketio import SocketIOConfig


class WorkerSdkConfig(BaseModel):
    socket_config: SocketIOConfig | None = None

    class Config:
        extra = Extra.forbid
        allow_mutation = False
        frozen = True
        arbitrary_types_allowed = True
