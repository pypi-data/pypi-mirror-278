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
        serialized_context = {}

        if "task_instance" in context and isinstance(
            context["task_instance"], TaskInstance
        ):
            task_instance = context["task_instance"]
            task_instance_context = {
                "task_id": task_instance.task_id,
                "dag_id": task_instance.dag_id,
                "execution_date": str(task_instance.execution_date),
                "start_date": str(task_instance.start_date),
                "end_date": str(task_instance.end_date),
                "state": task_instance.state,
                "try_number": task_instance.try_number,
                "hostname": task_instance.hostname,
                "max_tries": task_instance.max_tries,
                "pool": task_instance.pool,
                "priority_weight": task_instance.priority_weight,
                "queue": task_instance.queue,
                "operator": task_instance.operator,
                "duration": task_instance.duration,
                "queued_dttm": str(task_instance.queued_dttm),
                "pid": task_instance.pid,
                "log_url": task_instance.log_url,
                "external_executor_id": task_instance.external_executor_id,
            }
            serialized_context["task_instance"] = task_instance_context

        if "dag" in context and isinstance(context["dag"], DAG):
            dag = context["dag"]
            dag_context = {
                "dag_id": dag.dag_id,
                "start_date": str(dag.start_date),
                "end_date": str(dag.end_date),
                "schedule_interval": str(dag.schedule_interval),
                "catchup": dag.catchup,
                "is_paused_upon_creation": dag.is_paused_upon_creation,
                "default_args": dag.default_args,
                "description": dag.description,
                "is_subdag": dag.is_subdag,
                "fileloc": dag.fileloc,
                "concurrency": dag.concurrency,
                "max_active_tasks": dag.max_active_tasks,
                "max_active_runs": dag.max_active_runs,
            }
            serialized_context["dag"] = dag_context

        return serialized_context

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
