from ._mock import MockType
from .base import Base


# class TargetSearch(BaseModel):
#     keyword: str = ""
#     person_name: str = ""
#     person_level_ids: list = []
#     person_type_ids: list = []
#     sack_start_time: str = ""
#     sack_end_time: str = ""
#     sort_sacking_time: str = ""
#     is_enable: int = None
#     is_picture: int = None  # （0全部;1存在目标图片;2不存在）
#     is_positive: int = None  # (0:正面人物，1:非正面人物)
#     page: int = 1
#     page_size: int = 100000


class Target(Base, metaclass=MockType):
    def __init__(self, baseurl='http://targetapi-prod:8000', transport=None):
        super().__init__(baseurl, transport)

    def search(
            self, *,
            keyword: str = "",
            person_id: str = "",
            person_name: str = "",
            person_level_ids=None,
            person_type_ids=None,
            sack_start_time: str = "",
            sack_end_time: str = "",
            sort_sacking_time: str = "",
            is_enable: int = None,
            is_picture: int = None,  # (0全部;1存在目标图片;2不存在)
            is_positive: int = None,  # (0:正面人物，1:非正面人物)
            page: int = 1,
            page_size: int = 100000,
    ):
        if person_type_ids is None:
            person_type_ids = []
        if person_level_ids is None:
            person_level_ids = []

        data = {
            "keyword": keyword,
            "person_id": person_id,
            "person_name": person_name,
            "person_type_ids": person_type_ids,
            "person_level_ids": person_level_ids,
            "sack_start_time": sack_start_time,
            "sack_end_time": sack_end_time,
            "sort_sacking_time": sort_sacking_time,
            "is_enable": is_enable,
            "is_picture": is_picture,
            "is_positive": is_positive,
            "page_size": page_size,
            "page": page,
        }

        info = self._do_post('target/search', data)

        return info["result_list"]

    def get_by_ids(self, *, person_ids: list):
        data = {"person_ids": person_ids}
        info = self._do_post('target/get_by_ids', data)
        return info["result_list"]

    def connect_add_by_feature(self, *, person_name: str, feature: list, is_force: bool, person_id: str):
        data = {
            "person_name": person_name,
            "feature": feature,
            "is_force": is_force,
            "person_id": person_id
        }
        info = self._do_post('target/connect_add_by_feature', data)
        return info["person_ids"], info["is_indb"]

    def connect_get_info(self, *, connect_id: int) -> (dict, list):
        data = {
            "connect_id": connect_id
        }
        info = self._do_post('target/connect_get_info', data)
        return info["info"], info["pictures"]

    def add_exclude(self, *, person_feature: list) -> list:
        data = person_feature
        # self.baseurl = "http://targetapi-feature-prod:8000"
        result = self._do_post('feature/exclude/add', data)
        return result["success"]

    def remove_exclude(self, *, person_feature: list) -> list:
        data = person_feature
        # self.baseurl = "http://targetapi-feature-prod:8000"
        result = self._do_post('feature/exclude/remove', data)
        return result["success"]

    def add_include(self, *, person_feature: list) -> list:
        data = person_feature
        # self.baseurl = "http://targetapi-feature-prod:8000"
        result = self._do_post('feature/include/add', data)
        return result["success"]

    def remove_include(self, *, person_feature: list) -> list:
        data = person_feature
        # self.baseurl = "http://targetapi-feature-prod:8000"
        result = self._do_post('feature/include/remove', data)
        return result["success"]

    def base64_feature(self, *, img_base64: str):
        data = {
            "img_base64": img_base64
        }
        result = self._do_post('picture/base64_feature', data)
        return result["faces"]

    def target_add(
            self, *, person_id="", person_name: str, sacking_time: str, sacking_place: str, native_place: str,
            level: str, school: str, post: str, birth_date: str, remark: str, is_enable: int, is_positive: int,
            level_color: int, person_type_id: int, person_level_id: int
    ):
        data = {
            "person_id": person_id,
            "person_name": person_name,
            "sacking_time": sacking_time,
            "sacking_place": sacking_place,
            "native_place": native_place,
            "level": level,
            "school": school,
            "post": post,
            "birth_date": birth_date,
            "remark": remark,
            "is_enable": is_enable,
            "is_positive": is_positive,
            "level_color": level_color,
            "person_type_id": person_type_id,
            "person_level_id": person_level_id
        }
        result = self._do_post('target/add', data)
        return result["person_id"]

    def picture_add(self, *, person_id, img_base64, is_scan=1, feature_type=1):
        data = {
            "person_id": person_id,
            "img_base64": img_base64,
            "is_scan": is_scan,
            "feature_type": feature_type
        }
        result = self._do_post('picture/add', data)
        return result["picture_id"]

    def picture_search(self, *, person_id, feature_type=1, page=1, page_size=100000):
        data = {
            "page": page,
            "page_size": page_size,
            "person_id": person_id,
            "feature_type": feature_type
        }
        result = self._do_post('picture/search', data)
        return result["result_list"]
