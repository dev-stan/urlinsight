from pydantic import BaseModel

class LinkCreate(BaseModel):
    target_url: str

class LinkResponse(BaseModel):
    short_code: str
    target_url: str

    class Config:
        orm_mode = True  # Allows returning SQLAlchemy objects directly
