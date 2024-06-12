from __future__ import annotations

import datetime as _datetime
import hashlib
import logging
from dataclasses import asdict, dataclass
from functools import partial
from typing import Any, Callable, Dict, Iterable, List, Optional, Union

from flytekit.configuration import SerializationSettings
from flytekit.core import launch_plan as _annotated_launchplan
from flytekit.core import workflow as _annotated_workflow
from flytekit.core.base_task import TaskResolverMixin
from flytekit.core.python_function_task import PythonFunctionTask
from flytekit.core.resources import Resources
from flytekit.core.task import TaskPlugins
from flytekit.core.task import task as flytekit_task_decorator
from flytekit.image_spec import ImageSpec
from flytekit.models.documentation import Documentation
from flytekit.models.security import Secret

logger = logging.getLogger(__name__)


@dataclass
class ActorEnvironment:
    # I think we should add a user-defined name field here to help with entropy, but there are concerns also
    # These fields here are part of the actor config.
    container_image: Optional[Union[str, ImageSpec]] = None
    backlog_length: Optional[int] = None
    parallelism: Optional[int] = None
    replica_count: Optional[int] = None
    ttl_seconds: Optional[int] = None
    environment: Optional[Dict[str, str]] = None
    requests: Optional[Resources] = None
    limits: Optional[Resources] = None
    secret_requests: Optional[List[Secret]] = None

    def __call__(
        self,
        _task_function=None,
        cache: bool = False,
        cache_serialize: bool = False,
        cache_version: str = "",
        retries: int = 0,
        timeout: Union[_datetime.timedelta, int] = 0,
        node_dependency_hints: Optional[
            Iterable[
                Union[
                    PythonFunctionTask,
                    _annotated_launchplan.LaunchPlan,
                    _annotated_workflow.WorkflowBase,
                ]
            ]
        ] = None,
        task_resolver: Optional[TaskResolverMixin] = None,
        docs: Optional[Documentation] = None,
        **kwargs,
    ):
        wrapper = partial(
            flytekit_task_decorator,
            task_config=self,
            cache=cache,
            cache_serialize=cache_serialize,
            cache_version=cache_version,
            retries=retries,
            timeout=timeout,
            node_dependency_hints=node_dependency_hints,
            task_resolver=task_resolver,
            docs=docs,
            container_image=self.container_image,
            environment=self.environment,
            requests=self.requests,
            limits=self.limits,
            secret_requests=self.secret_requests,
            **kwargs,
        )

        if _task_function:
            return wrapper(_task_function=_task_function)
        return wrapper

    @property
    def environment_id(self) -> str:
        # TODO: Add proper entropy
        all_fields = "".join([str(getattr(self, f)) for f in asdict(self).keys()])
        hash_object = hashlib.md5(all_fields.encode("utf-8"))
        hex_digest = hash_object.hexdigest()
        logger.debug(f"Computing actor hash with string {all_fields} to {hex_digest[:15]}")
        return hex_digest[:15]

    @property
    def container_image_name(self) -> str:
        if isinstance(self.container_image, ImageSpec):
            return self.container_image.image_name()
        return self.container_image


class ActorTask(PythonFunctionTask[ActorEnvironment]):
    _ACTOR_TASK_TYPE = "fast-task"

    def __init__(self, task_config: ActorEnvironment, task_function: Callable, **kwargs):
        super(ActorTask, self).__init__(
            task_config=task_config,
            task_type=self._ACTOR_TASK_TYPE,
            task_function=task_function,
            **kwargs,
        )

    def get_custom(self, settings: SerializationSettings) -> Optional[Dict[str, Any]]:
        """
        Serialize the `ActorTask` config into a dict.

        :param settings: Current serialization settings
        :return: Dictionary representation of the dask task config.
        """
        return {
            "id": self.task_config.environment_id,
            "type": self._ACTOR_TASK_TYPE,
            "spec": {
                "container_image": self.task_config.container_image_name,
                "backlog_length": self.task_config.backlog_length,
                "parallelism": self.task_config.parallelism,
                "replica_count": self.task_config.replica_count,
                "ttl_seconds": self.task_config.ttl_seconds,
            },
        }


TaskPlugins.register_pythontask_plugin(ActorEnvironment, ActorTask)
