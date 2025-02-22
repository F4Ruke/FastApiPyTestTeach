from pydantic import BaseModel, Field
from src.models.user_data import RegistryUserDataRequest


class CreateApplicationRequest(BaseModel):
    user_id: int = Field(gt=0)


class CreateApplicationResponse(BaseModel):
    application_id: int = Field(gt=0)
    user: RegistryUserDataRequest


class CreateApplicationsResponse(BaseModel):
    applications: list[CreateApplicationResponse]


class DeleteApplicationRequest(BaseModel):
    application_id: int = Field(gt=0)