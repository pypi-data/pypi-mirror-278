from ..conf import API_TOKEN
from .core import ScraperAPI


class TikTok(ScraperAPI):
    dataset_id = "gd_lu702nij2f790tmv9h"

    def __init__(self, api_token: str = API_TOKEN):
        self.api_token = api_token
