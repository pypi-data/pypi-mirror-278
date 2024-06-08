import importlib
import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from task_manager.core.settings import get_setting

from .models import TaskManager

logger = logging.getLogger(__name__)

TOLERANCE = 10

PRIORITY = get_setting("TASK_MANAGER")


# do not use our own task decorator
@shared_task(bind=False, priority=PRIORITY)
def mark_task_as_cancelled(task_manager_id):
    logger.info(f"Running mark_task_as_cancelled for {task_manager_id}")

    x = TaskManager.objects.filter(id=task_manager_id).first()
    if x is None:
        logger.error(f"TaskManager {task_manager_id} not found")
        return

    if x.status not in ["PENDING", "PAUSED"]:
        logger.warning(f"TaskManager {task_manager_id} was already DONE")
        return

    x.status = "CANCELLED"
    x.save()

    logger.info(f"TaskManager {task_manager_id} is being marked as CANCELLED")


# do not use our own task decorator
@shared_task(bind=False, priority=PRIORITY)
def mark_task_as_reversed(task_manager_id, *, attempts=0, force=False):
    logger.info(f"Running mark_task_as_reversed for {task_manager_id}")

    x = TaskManager.objects.filter(id=task_manager_id).first()
    if x is None:
        logger.error(f"TaskManager {task_manager_id} not found")
        return

    if x.reverse_module is None or x.reverse_name is None:
        logger.warning(f"TaskManager {task_manager_id} does not have a reverse function")
        return

    if not force and (
        x.status != "DONE"
        and not x.last_run < timezone.now() - timedelta(minutes=TOLERANCE)
        and not x.killed
        and attempts < 10
    ):
        logger.warning(f"TaskManager {task_manager_id} was not killed, scheduling to run it again")

        x.status = "CANCELLED"
        x.save()

        mark_task_as_reversed.apply_async(
            args=(task_manager_id,), kwargs={"attempts": attempts + 1}, eta=timezone.now() + timedelta(seconds=30)
        )
        return

    x.status = "REVERSED"
    x.save()

    module = importlib.import_module(x.reverse_module)
    function = getattr(module, x.reverse_name)
    function(*x.arguments["args"], **x.arguments["kwargs"])

    logger.info(f"TaskManager {task_manager_id} is being marked as REVERSED")


# do not use our own task decorator
@shared_task(bind=False, priority=PRIORITY)
def mark_task_as_paused(task_manager_id):
    logger.info(f"Running mark_task_as_paused for {task_manager_id}")

    x = TaskManager.objects.filter(id=task_manager_id).first()
    if x is None:
        logger.error(f"TaskManager {task_manager_id} not found")
        return

    if x.status != "PENDING":
        logger.warning(f"TaskManager {task_manager_id} is not running")
        return

    x.status = "PAUSED"
    x.save()

    logger.info(f"TaskManager {task_manager_id} is being marked as PAUSED")


# do not use our own task decorator
@shared_task(bind=False, priority=PRIORITY)
def mark_task_as_pending(task_manager_id, *, attempts=0, force=False, last_run=None):
    logger.info(f"Running mark_task_as_pending for {task_manager_id}")

    x = TaskManager.objects.filter(id=task_manager_id).first()
    if x is None:
        logger.error(f"TaskManager {task_manager_id} not found")
        return

    if x.status in ["DONE", "CANCELLED", "REVERSED"]:
        logger.warning(f"TaskManager {task_manager_id} was already DONE")
        return

    if last_run and last_run != x.last_run:
        logger.warning(f"TaskManager {task_manager_id} is already running")
        return

    tolerance = TOLERANCE
    if x.status == "SCHEDULED":
        tolerance *= 3

    if (
        force is False
        and not x.last_run < timezone.now() - timedelta(minutes=tolerance)
        and not x.killed
        and attempts < 10
    ):
        logger.warning(f"TaskManager {task_manager_id} was not killed, scheduling to run it again")

        mark_task_as_pending.apply_async(
            args=(task_manager_id,),
            kwargs={
                "attempts": attempts + 1,
                "last_run": last_run or x.last_run,
            },
            eta=timezone.now() + timedelta(seconds=30),
        )
        return

    x.status = "PENDING"
    x.killed = False
    x.save()

    module = importlib.import_module(x.task_module)
    function = getattr(module, x.task_name)
    function.delay(
        *x.arguments["args"],
        **{
            **x.arguments["kwargs"],
            "page": x.current_page + 1,
            "total_pages": x.total_pages,
            "task_manager_id": task_manager_id,
        },
    )

    logger.info(f"TaskManager {task_manager_id} is being marked as PENDING")


MODULES = {}
