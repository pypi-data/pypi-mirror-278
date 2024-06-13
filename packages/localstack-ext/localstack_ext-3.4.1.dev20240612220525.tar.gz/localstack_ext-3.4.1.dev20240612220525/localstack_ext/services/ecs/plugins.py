import logging
from typing import Any
from localstack_ext import config as config_ext
from localstack_ext.runtime.plugin import ProPlatformPlugin
LOG=logging.getLogger(__name__)
class EcsK8sPlatformPlugin(ProPlatformPlugin):
	name='ecs-k8s-task-executor';requires_license=True
	def on_service_load(B,service,provider):
		from localstack_ext.services.ecs.task_executors.kubernetes import ECSTaskExecutorKubernetes as A
		if service!='ecs':return
		provider.task_executor=A();LOG.info('Configured ECS service to use kubernetes task executor')
	def should_load(A):
		if not super().should_load():return False
		return config_ext.ECS_TASK_EXECUTOR=='kubernetes'