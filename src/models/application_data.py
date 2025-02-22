from pydantic import BaseModel, Field
from src.models.user_data import RegistryUserDataRequest


class CreateApplicationRequest(BaseModel):
    user_id: int = Field(gt=0)


class CreateApplicationResponse(BaseModel):
    id: int = Field(gt=0)
    user: RegistryUserDataRequest


class CreateApplicationsResponse(BaseModel):
    applications: list[CreateApplicationResponse]