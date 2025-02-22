import uvicorn
from time import sleep
from random import randint
from fastapi import FastAPI, HTTPException
from sys import path as sys_path
from os import path as os_path

sys_path.append(os_path.abspath(os_path.curdir))

from src.models.user_data import UsersDataResponse, UserDataResponse, RegistryUserDataRequest, RegistryUsersDataResponse, Role
from src.database.users import users_list
from src.database.application import application_list
from src.models.application_data import CreateApplicationResponse, CreateApplicationRequest, CreateApplicationsResponse
from src.helpers.generate import UserData

app = FastAPI()


@app.get(
    path="/generate_users/{count_users}",
    summary="Генерация пользователей.",
    tags=["Подготовка данных"],
    response_model=UsersDataResponse
)
def generate_users(count_users: int) -> UsersDataResponse:
    """Возвращает случайно сгенерируемых пользователей."""
    temp_users = []

    for _ in range(count_users):
        data = UserData()

        temp_users.append(
            UserDataResponse(
                first_name=data.first_name,
                last_name=data.last_name,
                middle_name=data.middle_name,
                full_name=data.full_name,
                sex=data.sex,
                role=data.role,
                email=data.email,
                age=data.age,
                password=data.password
            )
        )

    return UsersDataResponse(users=temp_users)


@app.post(path="/registry_user", summary="Регистрация пользователей.", tags=["Регистрация"])
def post_registry_user(user_data_req: UserDataResponse) -> dict:
    """Регистрирует пользователя."""
    users_list.append(RegistryUserDataRequest(user_id=len(users_list) + 1, **user_data_req.model_dump()))

    return {}


@app.get(path="/registry_users", summary="Получение всех зарегистрированных пользователей.", tags=["Получение данных"])
def get_registry_users() -> RegistryUsersDataResponse:
    """Возвращаем зарегистрированных пользователей."""
    return RegistryUsersDataResponse(users=users_list)


@app.post(path="/create_application", summary="Создание заявки.", tags=["Заявка"], response_model=CreateApplicationsResponse)
def create_application(app_req: CreateApplicationRequest) -> CreateApplicationsResponse:
    """Создаем заявку."""
    if users := [user for user in users_list if app_req.user_id == user.user_id]:
        for user in users:
            if user.role != Role.DIRECTOR.value:
                raise HTTPException(status_code=403, detail=f"Заявку может создать только пользователь с ролью директор.")

            sleep(randint(10, 20))

            application_list.append(CreateApplicationResponse(id=len(application_list) + 1, user=user))
    else:
        raise HTTPException(status_code=403, detail=f"Пользователь не зарегистирован.")

    return CreateApplicationsResponse(applications=application_list)


@app.get(
    path="/applications",
    summary="Получение активных заявок.",
    tags=["Заявка"],
    response_model=CreateApplicationsResponse
)
def create_application() -> CreateApplicationsResponse:
    """Создаем заявку."""
    return CreateApplicationsResponse(applications=application_list)


if __name__ == "__main__":
    uvicorn.run(app="src.api.api:app", reload=True)
