from app.search.api import BaseSearchAPI


class RecordAPI(BaseSearchAPI):
    api_path = "/records/"

    def __init__(self, record_id):
        super().__init__()
        self.api_path = f"{self.api_path}{record_id}/"
