from fastapi.security import OAuth2AuthorizationCodeBearer
from fief_client import FiefAsync
from fief_client.integrations.fastapi import FiefAuth

from typing import List


class UserService:
    def __init__(self, user_repository: SqlAlchemyRepository) -> None:
        self._repository: SqlAlchemyRepository = user_repository

    def create_user(self, user: UserCreate) -> User:
        created_user: User = self._repository.create_user(user)

        return created_user

    def get_user_by_id(self, user_id: str) -> User:
        user: User = self._repository.get_user_by_id(user_id)
        return user

    def list_users(self) -> List[User]:
        users_list = self._repository.list_users()

        return users_list

    def verify_user(self, user: UserAuthenticate) -> bool:
        return self._repository.verify_user(user)
