import yaml, os, codecs
from .singleton import singleton


@singleton
class ConfigSingleton:
    def __init__(self, common_config_dir=None, branch_config_dir=None):
        common = self.load_config(common_config_dir)
        branch = self.load_config(branch_config_dir)
        self.config = {**common, **branch}
        assert len(self.config), 'Error: empty config!'

    def get(self):
        return self.config

    @staticmethod
    def load_config(path=None):
        if path is not None:
            if path.endswith('/'): 
                path = path[:-1]
            assert os.path.exists(path), 'Error: config unavailable!'
            with codecs.open(f'{path}/config.yaml', encoding='utf-8') as file:
                return yaml.load(file, yaml.Loader)
        return {}
