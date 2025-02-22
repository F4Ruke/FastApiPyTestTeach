from pydantic import BaseModel, Field, EmailStr

from src.constants.user_data import Sex, Role


class UserDataResponse(BaseModel):
    id: int = Field(gt=0)
    sex: str | Sex
    first_name: str = Field(min_length=3, max_length=30)
    last_name: str = Field(min_length=3, max_length=30)
    middle_name: str = Field(min_length=3, max_length=30)
    full_name: str = Field(min_length=6, max_length=100)
    role: str | Role
    email: EmailStr
    age: int = Field(ge=18)
    password: str = Field(min_length=6)


class UsersDataResponse(BaseModel):
    users: list[UserDataResponse]


class PasswordDataRequest(BaseModel):
    password: str = Field(min_length=6, max_length=30)


class RegistryUserDataRequest(PasswordDataRequest, UserDataResponse):
    pass


class RegistryUsersDataResponse(BaseModel):
    users: list[RegistryUserDataRequest]