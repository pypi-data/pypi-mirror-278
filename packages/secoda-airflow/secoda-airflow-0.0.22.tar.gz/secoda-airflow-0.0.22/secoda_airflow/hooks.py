import requests

from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook
from airflow.models import TaskInstance, DAG


class SecodaHook(BaseHook):
    conn_name_attr = "secoda_conn_id"
    default_conn_name = "secoda_default"
    conn_type = "secoda"
    hook_name = "Secoda Hook"

    def __init__(self, context, *args, **kwargs):
        super().__init__(*args, **kwargs)

        secoda_conn_id = self.default_conn_name
        custom_conn_id = context["dag"].params.get("secoda_conn_id")
        if custom_conn_id:
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

    def serialize_context(self, context):
        if isinstance(context, TaskInstance):
            return {
                "task_id": context.task_id,
                "dag_id": context.dag_id,
                "execution_date": str(context.execution_date),
                "start_date": str(context.start_date),
                "end_date": str(context.end_date),
                "state": context.state,
                "try_number": context.try_number,
                "hostname": context.hostname,
                "max_tries": context.max_tries,
                "pool": context.pool,
                "priority_weight": context.priority_weight,
                "queue": context.queue,
                "operator": context.operator,
                "duration": context.duration,
                "queued_dttm": str(context.queued_dttm),
                "pid": context.pid,
                "log_url": context.log_url,
                "external_executor_id": context.external_executor_id,
            }
        elif isinstance(context, DAG):
            return {
                "dag_id": context.dag_id,
                "start_date": str(context.start_date),
                "end_date": str(context.end_date),
                "schedule_interval": str(context.schedule_interval),
                "catchup": context.catchup,
                "is_paused_upon_creation": context.is_paused_upon_creation,
                "default_args": context.default_args,
                "description": context.description,
                "is_subdag": context.is_subdag,
                "fileloc": context.fileloc,
                "concurrency": context.concurrency,
                "max_active_tasks": context.max_active_tasks,
                "max_active_runs": context.max_active_runs,
            }

        return {}

    def post(self, endpoint: str, data: dict) -> requests.Response:
        return requests.post(
            f"{self.sanitized_host}{endpoint}",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=data,
        )

    def post_task_success(self, context):
        return self.post(
            f"/integration/run_logs/{self.integration_id}/ingest/",
            self.serialize_context(context),
        )

    def post_dag_success(self, context):
        return self.post(
            f"/integration/run_logs/{self.integration_id}/ingest/",
            self.serialize_context(context),
        )

    def post_task_failure(self, context):
        return self.post(
            f"/integration/run_logs/{self.integration_id}/ingest/",
            self.serialize_context(context),
        )

    def post_dag_failure(self, context):
        return self.post(
            f"/integration/run_logs/{self.integration_id}/ingest/",
            self.serialize_context(context),
        )
