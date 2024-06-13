from ._mock import MockType
from .base import Base
from typing import List


class System(Base, metaclass=MockType):
    def __init__(self, baseurl="http://systemapi-prod:8000", transport=None):
        super().__init__(baseurl, transport)

    def add_role(
        self,
        *,
        name: str,
        template_ids: List[int],
        is_active: bool = True,
        memo: str = "",
    ):
        payload = {
            "name": name,
            "template_ids": template_ids,
            "is_active": is_active,
            "memo": memo,
        }

        response = self._do_post("add_role", payload)
        return response["id"]

    def edit_role(
        self,
        *,
        id: int,
        name: str,
        template_ids: List[int],
        is_active: bool = True,
        memo: str = "",
    ):
        payload = {
            "id": id,
            "name": name,
            "template_ids": template_ids,
            "is_active": is_active,
            "memo": memo,
        }

        response = self._do_post("edit_role", payload)
        return response["result"]

    def reset_password(self, *, id: int, password: str):
        payload = {"id": id, "password": password}

        response = self._do_post("reset_password", payload)
        return response["result"]
