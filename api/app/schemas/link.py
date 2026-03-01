from pydantic import BaseModel, ConfigDict


class LinkCreate(BaseModel):
    target_url: str


class LinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    short_code: str
    target_url: str
