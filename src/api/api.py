import uvicorn
from time import sleep
from random import randint
from fastapi import FastAPI, HTTPException
from sys import path as sys_path
from os import path as os_path

sys_path.append(os_path.abspath(os_path.curdir))

from src.models.user_data import UsersDataResponse, UserDataResponse, RegistryUserDataRequest, \
    RegistryUsersDataResponse, Role, DeleteUserRequest
from src.database.users import users_list
from src.database.application import application_list
from src.models.application_data import CreateApplicationResponse, CreateApplicationRequest, CreateApplicationsResponse, \
    DeleteApplicationRequest
from src.helpers.generate import UserData

app = FastAPI()


@app.get(
    path="/generate_users",
    summary="Генерация пользователей.",
    tags=["Пользователь"],
    response_model=UsersDataResponse
)
def generate_users(count_users: int = 1) -> UsersDataResponse:
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


@app.post(path="/registry_user", summary="Регистрация пользователя.", tags=["Пользователь"])
def post_registry_user(user_data_req: UserDataResponse) -> dict:
    """Регистрирует пользователя."""
    users_list.append(RegistryUserDataRequest(user_id=len(users_list) + 1, **user_data_req.model_dump()))

    return {}


@app.get(path="/registry_users", summary="Получение всех зарегистрированных пользователей.", tags=["Пользователь"])
def get_registry_users() -> RegistryUsersDataResponse:
    """Возвращаем зарегистрированных пользователей."""
    return RegistryUsersDataResponse(users=users_list)


@app.delete(path="/registry_user", summary="Удаление пользователя.", tags=["Пользователь"])
def delete_user(user_id_data: DeleteUserRequest) -> dict:
    """Удаляем пользователя из списка зарегистрированных пользователей."""
    for i, user in enumerate(users_list):
        if user_id_data.user_id == user.user_id:
            del users_list[i]
            return {}

    raise HTTPException(status_code=404, detail="Пользователь не найдена.")


@app.post(
    path="/create_application", summary="Создание заявки.", tags=["Заявка"], response_model=CreateApplicationsResponse
)
def create_application(app_req: CreateApplicationRequest) -> CreateApplicationsResponse:
    """Создаем заявку."""

    if user_data := [user for user in users_list if app_req.user_id == user.user_id]:
        if user_data[0].role == Role.DIRECTOR.value or user_data[0].role == Role.USER.value:
            sleep(randint(10, 20))
            application_list.append(
                CreateApplicationResponse(application_id=len(application_list) + 1, user=user_data[0])
            )
        else:
            raise HTTPException(status_code=403, detail="Заявку может создать только пользователь с ролью директор.")
    else:
        raise HTTPException(status_code=403, detail="Пользователь не зарегистирован.")

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


@app.delete(path="/application", summary="Удаление заявки.", tags=["Заявка"])
def delete_application(app_id_data: DeleteApplicationRequest) -> dict:
    """Удаляем заявку."""
    for i, application in enumerate(application_list):
        if app_id_data.application_id == application.application_id:
            del application_list[i]
            return {}

    raise HTTPException(status_code=404, detail="Заявка не найдена.")


if __name__ == "__main__":
    print("Open current URL: http://127.0.0.1:8000/docs")
    uvicorn.run(app="src.api.api:app", reload=True)
