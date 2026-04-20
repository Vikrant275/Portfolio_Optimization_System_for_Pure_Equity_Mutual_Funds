import yaml
import os,sys
from framework.exception import MyException
from framework.constant import *



class GetConfig:
    def __init__(self,config_file:str=None,variables:str=None):
        self.config_file = config_file
        self.variables = variables

    def load_config(self):
        config_path = os.path.join(CONFIG_PATH, self.config_file)

        with open(config_path, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        if config is None:
            raise MyException(f"No config file at {CONFIG_PATH}")
        else:
            return config

    def get(self):
        try:
            if self.variables and self.config_file is not None:
                config = self.load_config()

                content = config.get(self.variables,{})
                if content is None:
                    raise MyException(f"No config file at {self.config_file}")
                else:
                    return content
        except Exception as e:
            raise MyException(e,sys)

