
import os
import yaml


class Config(object):

    def __init__(self, config):
        self._config = config

    def __repr__(self):
        return repr(self._config)

    def __getattr__(self, key):
        if key in self._config:
            return self._config[key]

    def get(self, *args, **kwargs):
        return self._config.get(*args, **kwargs)


_config = None


def load():
    global _config
    if _config is not None:
        return _config
    data = None
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yml')
    with open(config_path) as f:
        data = yaml.load(f)
    config = data.get('common', {})
    flavor = os.environ.get('SETTINGS_FLAVOR', 'dev')
    config.update(data.get(flavor, {}))
    config['flavor'] = flavor
    load_environment_variables(config)
    _config = Config(config)
    return _config

def load_environment_variables(config):
    env_variables = {
        's3_access_key': os.environ.get("DOCKER_S3_ACCESS_KEY"),
        's3_secret_key': os.environ.get("DOCKER_S3_SECRET_KEY"),
        's3_bucket':     os.environ.get("DOCKER_S3_BUCKET"),
        'storage':       os.environ.get("DOCKER_STORAGE"),
        'storage_path':  os.environ.get("DOCKER_STORAGE_PATH"),
        'loglevel':      os.environ.get("DOCKER_LOGLEVEL"),
        'secret_key':    os.environ.get("DOCKER_SECRET_KEY")
    }
    config.update(without_empty_values(env_variables))

    email_exceptions_env_variables = {
        'smtp_host':     os.environ.get("DOCKER_EMAIL_EXCEPTIONS_SMTP_HOST"),
        'smtp_login':    os.environ.get("DOCKER_EMAIL_EXCEPTIONS_SMTP_LOGIN"),
        'smtp_password': os.environ.get("DOCKER_EMAIL_EXCEPTIONS_SMTP_PASSWORD"),
        'from_addr':     os.environ.get("DOCKER_EMAIL_EXCEPTIONS_FROM_ADDR"),
        'to_addr':       os.environ.get("DOCKER_EMAIL_EXCEPTIONS_TO_ADDR")
    }
    config.setdefault('email_exceptions', {}).update(without_empty_values(email_exceptions_env_variables))

def without_empty_values(items):
    return dict((k, v) for k, v in items.iteritems() if v)
