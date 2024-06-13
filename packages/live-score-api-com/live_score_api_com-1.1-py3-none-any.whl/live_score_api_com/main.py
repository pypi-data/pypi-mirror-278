import requests
from requests.exceptions import HTTPError
import time


class LiveScoreAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://livescore-api.com/api-client"

    def _make_request(self, endpoint, params):
        max_retries = 3
        backoff_factor = 2  # constant which is used for exponential backoff strategy
        retries = 0
        wait = 1  # Initial wait time (s)

        while retries < max_retries:
            url = f"{self.base_url}{endpoint}"
            params.update({"key": self.api_key, "secret": self.api_secret})

            try:
                response = requests.get(url, params=params)
                response.raise_for_status()  # Raise an exception for non-2xx status codes
                response_data = response.json()
                if 'data' in response_data:
                    return response_data["data"]
                else:
                    raise ValueError("Invalid response structure")

            except HTTPError as e:
                if 500 <= e.response.status_code < 600:  # Server error (5xx)
                    retries += 1
                    wait_time = wait * (backoff_factor ** (retries - 1))
                    print(f"Server error, retrying in {wait_time} seconds... (Retry {retries}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    raise e

        raise Exception(f"Maximum retries exceeded for the API request.")

    def _get_params(self, **kwargs):
        filtered_params = {}
        for k, v in kwargs.items():
            if v is not None:
                filtered_params[k] = v
        return filtered_params

