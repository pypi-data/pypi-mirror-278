from pydantic import BaseModel, ConfigDict


class BRD(BaseModel):
    model_config = ConfigDict(extra="forbid")
