import requests


class ApiClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    @staticmethod
    def handle_response(response, status):
        if (len(status) == 0 and 100 < response.status_code < 400) or (
            len(status) > 0 and response.status_code in status
        ):
            return response
        else:
            try:
                response = response.json()
            except Exception:
                pass
            raise requests.HTTPError(response)

    def get(self, url, *args, **kwargs):
        status = kwargs.pop("status", {})
        response = requests.get(self.base_url + str(url), *args, **kwargs)
        return self.handle_response(response, set() if status is None else status)
