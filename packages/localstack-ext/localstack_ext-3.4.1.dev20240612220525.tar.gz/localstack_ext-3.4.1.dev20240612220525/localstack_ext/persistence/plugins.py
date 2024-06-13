import logging,os
from localstack import config
from localstack.runtime import hooks
from localstack.services.internal import get_internal_apis
from localstack_ext import config as config_ext
LOG=logging.getLogger(__name__)
@hooks.on_infra_start(should_load=config_ext.ACTIVATE_PRO)
def register_restricted_pods_api():from localstack_ext.persistence.pods.api.pods_api import CloudPodsRestrictedApi as A;get_internal_apis().add(A())
@hooks.on_infra_start(should_load=config_ext.ACTIVATE_PRO)
def register_remotes_pods_api():from localstack_ext.persistence.remotes.api import CloudPodsRemotesApi as A;get_internal_apis().add(A())
@hooks.on_infra_start(should_load=config_ext.ACTIVATE_PRO)
def register_ci_run_manager():from localstack_ext.utils.cloud_pods.ci_run_manager import get_ci_run_manager as A;A().startup()
@hooks.on_infra_shutdown(should_load=config_ext.ACTIVATE_PRO)
def shutdown_ci_run_manager():from localstack_ext.utils.cloud_pods.ci_run_manager import get_ci_run_manager as A;A().shutdown()
@hooks.on_infra_ready(should_load=config_ext.ACTIVATE_PRO)
def register_auto_load_pod():
	from localstack_ext.config import AUTO_LOAD_POD as A;from localstack_ext.persistence.pods.auto_load import PodLoaderFromEnv as D,PodLoaderFromInitDir as E;B=os.path.normpath(os.path.join(config.dirs.config,'..','init-pods.d'))
	if(A or os.path.exists(B))and config.PERSISTENCE:LOG.debug('AUTO_LOAD_POD has not effect if PERSISTENCE is enabled.');return
	if os.path.exists(B):C=E(init_dir=B);C.load()
	if A:C=D(A);C.load()