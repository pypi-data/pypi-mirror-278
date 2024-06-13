import logging
from datetime import datetime, timedelta
from typing import Dict, List

from ._mock import MockType
from .base import Base

__all__ = ["Dictionary", "DictionaryOption"]


class Option:
    def __init__(self, option_key: str, option_value: str):
        self.option_key = option_key
        self.option_value = option_value


class Dictionary(Base, metaclass=MockType):
    def __init__(self, baseurl='http://dictionary-prod:8000', transport=None):
        super().__init__(baseurl, transport)

    def get_dict_info(self, *, name: str, is_active: bool = True) -> dict:
        logging.warning("DeprecationWarning: Deprecated since v0.0.9. Use get_item() instead.")
        data = {
            'name': name,
            'is_active': is_active,
        }
        info = self._do_post('get_dict_info', data)
        result = {}
        for row in info["result_list"]:
            result[row["option_key"]] = row["option_value"]

        return result

    # def get_dict_by_ids(self, *, ids: list):
    #     data = {'ids': ids}
    #     info = self._do_post('/get_dict_by_ids', data)
    #     return info["result_list"]
    #
    # def get_option_by_ids(self, *, ids: list):
    #     data = {'ids': ids}
    #     info = self._do_post('/get_option_by_ids', data)
    #     return info["result_list"]

    def new_id(self, *, name: str, namespace: str):
        data = {
            'name': name,
            'namespace': namespace,
        }

        value_id = self._do_post('new_id', data, resp_jsonable=False)
        return value_id


class DictionaryOption(Base, metaclass=MockType):
    def __init__(self, name, *, baseurl='http://dictionary-prod:8000', expire=3600, transport=None):
        super().__init__(baseurl, transport)
        self.updated_at: datetime = datetime(1970, 1, 1)
        self.options: Dict[str, Option] = {}
        self.name = name
        self.expire = expire

    def _check_for_update(self, is_active: bool):
        if datetime.now() - self.updated_at >= timedelta(seconds=self.expire):
            data = {
                'name': self.name,
                'is_active': is_active,
            }
            info = self._do_post('get_dict_info', data)
            self.options = {}
            for item in info["result_list"]:
                key = str(item["option_key"])
                self.options[key] = Option(key, item["option_value"])

            self.updated_at = datetime.now()

    def get_item(self, *, key: str, is_active: bool = True) -> Option:
        self._check_for_update(is_active)

        return self.options.get(key)

    def get_items(self, *, is_active: bool = True) -> List[Option]:
        self._check_for_update(is_active)

        return list(self.options.values())
