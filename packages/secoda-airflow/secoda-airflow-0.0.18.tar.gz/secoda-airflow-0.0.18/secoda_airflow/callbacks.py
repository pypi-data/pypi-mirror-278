import logging
import traceback

from secoda_airflow.hooks import SecodaHook


logger = logging.getLogger(__name__)


def task_success_callback(context):
    try:
        hook = SecodaHook(context)
        hook.post(context)
    except Exception as e:
        logger.warning(
            f"Failed to send callback to Secoda: {e}\n{traceback.format_exc()}"
        )


def dag_success_callback(context):
    try:
        hook = SecodaHook(context)
        hook.post(context)
    except Exception as e:
        logger.warning(
            f"Failed to send callback to Secoda: {e}\n{traceback.format_exc()}"
        )


def task_failure_callback(context):
    try:
        hook = SecodaHook(context)
        hook.post(context)
    except Exception as e:
        logger.warning(
            f"Failed to send callback to Secoda: {e}\n{traceback.format_exc()}"
        )


def dag_failure_callback(context):
    try:
        hook = SecodaHook(context)
        hook.post(context)
    except Exception as e:
        logger.warning(
            f"Failed to send callback to Secoda: {e}\n{traceback.format_exc()}"
        )


task_callbacks = {
    "on_failure_callback": task_failure_callback,
    "on_success_callback": task_success_callback,
}

dag_callbacks = {
    "on_success_callback": dag_success_callback,
    "on_failure_callback": dag_failure_callback,
}
