import requests

from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook


class SecodaHook(BaseHook):
    conn_name_attr = "secoda_conn_id"
    default_conn_name = "secoda_default"
    conn_type = "secoda"
    hook_name = "Secoda Hook"

    def __init__(self, context, *args, **kwargs):
        super().__init__(*args, **kwargs)

        secoda_conn_id = self.default_conn_name
        if custom_conn_id := context["dag"].params.get("secoda_conn_id"):
            secoda_conn_id = custom_conn_id

        conn = self.get_connection(secoda_conn_id)
        self.api_key = conn.password
        self.host = conn.host or "https://api.secoda.com"
        self.integration_id = conn.extra_dejson.get("integration_id")

        if not self.api_key:
            raise AirflowException("No API key provided")

        if not self.integration_id:
            raise AirflowException("No integration ID provided")

    @property
    def sanitized_host(self) -> str:
        if self.host.endswith("/"):
            return self.host[:-1]

        return self.host

    def post(self, endpoint: str, data: dict) -> requests.Response:
        return requests.post(
            f"{self.sanitized_host}{endpoint}",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=data,
        )
