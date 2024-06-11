import os
from .api_client import APIClientBase, InvalidInputException


class Jobs(APIClientBase):
    def __init__(self, url_base=None, **kwargs):
        super().__init__(url_base or os.environ.get("PROTECTION_SERVICE", ""), **kwargs)

    def get_jobs(self):
        return self.get_request("/jobs")

    def get_job(self, id: str):
        if not id:
            raise InvalidInputException(f"Expected a valid job id, received: `{id}`")
        return self.get_request("/jobs/{id}", id=id)

    def create_job(self, body: dict):
        return self.post_request("/jobs", body=body)

    def patch_job(self, id: str, body: dict):
        if not id:
            raise InvalidInputException(f"Expected a valid job id, received: `{id}`")
        return self.patch_request("/jobs/{id}", id=id, body=body)

    def delete_job(self, id: str):
        if not id:
            raise InvalidInputException(f"Expected a valid job id, received: `{id}`")
        return self.delete_request("/jobs/{id}", id=id)
