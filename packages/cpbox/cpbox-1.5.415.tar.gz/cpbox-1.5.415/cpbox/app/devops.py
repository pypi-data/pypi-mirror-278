import os
import socket
import sys
from pathlib import Path

from cpbox.app.appconfig import appconfig
from cpbox.tool import file
from cpbox.tool import functocli
from cpbox.tool import logger
from cpbox.tool import spec
from cpbox.tool import system
from cpbox.tool import template
from cpbox.tool import utils

is_windows = os.name == 'nt'

class DevOpsAppConfig:

    def __init__(self, app_name, provider):
        appconfig.init(app_name, provider.get_env(), provider.get_app_config())


class DevOpsAppConfigProvider:

    def __init__(self, app_name):
        self.app_name = app_name
        default_data_dir = '/opt/data' if not is_windows else 'D:\\opt\\data'
        data_dir = Path(os.environ.get('CPBOX_DATA_DIR', default_data_dir))
        self.app_storage_dir = data_dir / app_name
        self.app_persistent_storage_dir = self.app_storage_dir / 'persistent'
        self.app_runtime_storage_dir = self.app_storage_dir / 'runtime'
        self.app_logs_dir = self.app_runtime_storage_dir / 'logs'

    def get_root_dir(self):
        if hasattr(sys.modules['__main__'], '__file__'):
            root_dir = Path(sys.argv[0]).resolve().parent
            return root_dir
        else:
            root_dir = Path.cwd()
            return root_dir

    def get_roles_dir(self):
        return self.get_root_dir() / 'roles'

    def get_app_root_dir(self):
        app_root_dir = self.get_roles_dir() / self.app_name
        return app_root_dir

    def get_env(self):
        env = os.environ['PUPPY_ENV'] if 'PUPPY_ENV' in os.environ else 'dev'
        return env

    def get_app_config(self):
        return {}

    def get_box_local_config(self):
        fn = self.get_root_dir() / '.box-local-config.yml'
        return utils.load_yaml(fn, {})

    def ensure_dir_and_write_permission(self):
        file.ensure_dir(self.app_storage_dir)
        file.ensure_dir(self.app_persistent_storage_dir)
        file.ensure_dir(self.app_runtime_storage_dir)
        file.ensure_dir(self.app_logs_dir)
        file.ensure_dir(self.app_logs_dir / 'syslog')


class DevOpsApp(object):

    def _want_logger_ex(self, **kwargs):
        logger.make_logger_for_app(self, **kwargs)
        logger_name = kwargs.get('log_config', {}).get('name', self.app_name)
        return logger.getLogger(logger_name)

    def __init__(self, app_name, log_level='info', exit_on_error=True, **kwargs):
        self.app_name = app_name

        self._init_app_config()

        self.log_level = log_level
        self.exit_on_error = exit_on_error
        self.logger = self._want_logger_ex(**kwargs)

        self.file_lock = None
        self._hostvar = None

    def _init_app_config(self):

        provider = self.create_app_config_provider()
        provider.ensure_dir_and_write_permission()

        hostname = socket.gethostname()
        self.hostname_fqdn = hostname
        self.hostname_short = hostname.split('.', 1)[0]

        self.env = provider.get_env()
        self.root_dir = provider.get_root_dir()
        self.roles_dir = provider.get_roles_dir()

        app_root_dir = provider.get_app_root_dir()
        self.app_root_dir = app_root_dir
        self.app_config_dir = app_root_dir / 'config'
        self.app_templates_dir = app_root_dir / 'templates'
        self.app_scripts_dir = app_root_dir / 'scripts'

        self.app_storage_dir = provider.app_storage_dir
        self.app_persistent_storage_dir = provider.app_persistent_storage_dir
        self.app_runtime_storage_dir = provider.app_runtime_storage_dir
        self.app_logs_dir = provider.app_logs_dir


    def create_app_config_provider(self):
        return DevOpsAppConfigProvider(self.app_name)

    def run_cmd_ret(self, cmd, log=True):
        return self.run_cmd(cmd, log=log)[1]

    def run_cmd(self, cmd, log=True):
        if log:
            self.logger.info('run_cmd: %s', cmd)
        return system.run_cmd(cmd)

    def shell_run(self, cmd, keep_pipeline=True, exit_on_error=True, dry_run=False, log=True):
        if log:
            self.logger.info('shell_run: %s', cmd)
        if dry_run:
            return 0
        exit_on_error = exit_on_error and self.exit_on_error
        return system.shell_run(cmd, keep_pipeline=keep_pipeline, exit_on_error=exit_on_error)

    def remove_container(self, name, force=False, dry_run=False):
        cmd = 'docker rm %s' % (name)
        if force:
            cmd = 'docker rm -f %s' % (name)
        self.shell_run(cmd, exit_on_error=False, dry_run=dry_run)

    def container_is_running(self, name):
        cmd = 'docker ps | grep %s' % (name)
        return self.run_cmd(cmd, log=False)[0] == 0

    def stop_container(self, name, timeout=300, dry_run=False):
        cmd = 'docker stop --time %d %s' % (timeout, name)
        self.shell_run(cmd, exit_on_error=False, dry_run=dry_run)

    def _check_lock(self):
        filepath = self.app_runtime_storage_dir / 'locks' / file.compute_lock_filepath(sys.argv)
        file_lock = file.obtain_lock(filepath)
        if file_lock is None:
            pid = 0
            with open(filepath, 'r') as f:
                pid = f.read()
            self.logger.warning('lock file exists, pid: %s => %s', pid, filepath)
            sys.exit(1)
        else:
            self.file_lock = file_lock

    def template_to(self, template_filename, dst, payload, app_name=None):
        template_payload = {'payload': payload}
        src = self.app_templates_dir_for(app_name) / template_filename
        template.render_to_file(src, template_payload, dst)
        self.logger.info('template_to: %s => %s', src, dst)

    def read_app_config(self, config_filebasename, app_name=None):
        if '.yml' not in config_filebasename:
            config_filebasename = config_filebasename + '.yml'
        data = utils.load_yaml(self.app_config_dir_for(app_name) / config_filebasename, {})
        return data

    def app_templates_dir_for(self, app_name=None):
        if app_name is None:
            return self.app_templates_dir
        return self.roles_dir / app_name / 'templates'

    def app_config_dir_for(self, app_name=None):
        if app_name is None:
            return self.app_config_dir
        return self.roles_dir / app_name / 'config'

    def get_group_names(self):
        return self.get_host_var().get('group_names', [])

    def get_configed_ops_scripts_dir(self):
        return self.get_host_var().get('ops_scripts_dir', '')

    def _read_hosts_var(self):
        fn = self.app_config_dir / 'hosts-var.yml'
        hosts_var = utils.load_yaml(fn, {})
        hostname = self.hostname_short
        return spec.LegacySpec(hosts_var, hostname).config_data

    def get_host_var(self):
        return {}

    def get_app_params(self, key=None, fallback=None):
        app_params = self.get_host_var().get('app_params', {})
        if key is None:
            return app_params
        return app_params.get(key, fallback)

    def get_global_params(self, key=None, fallback=None):
        global_params = self.get_host_var().get('global_params', {})
        if key is None:
            return global_params
        return global_params.get(key, fallback)

    @functocli.keep_method
    def check_health(self):
        print('%s is good' % (sys.argv[0]))

DevOpsApp.run_app = functocli.run_app