import os
import sys

import yaml
from dotenv import load_dotenv
from prodict import Prodict

load_dotenv('.env')


class Config(Prodict):
    DEFAULT = '../config.yaml'

    def __init__(self, name=None):
        if name:
            self._config_name = name
        else:
            self._config_name = sys.argv[1] if len(sys.argv) >= 2 else self.DEFAULT

        with open(self._config_name, 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
        super().__init__(**data)

    def env(self, name, default=''):
        return os.environ.get(name, default)

    def env_bool(self, name, default=False):
        val = self.env(name)
        val = str(val).upper()
        if val in ('1', 'TRUE', 'YES', 'Y'):
            return True
        elif val in ('0', 'FALSE', 'NO', 'N'):
            return False
        else:
            return default
