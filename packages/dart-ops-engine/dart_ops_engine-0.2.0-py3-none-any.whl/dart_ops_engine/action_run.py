from abc import ABC, abstractmethod
from typing import Dict, Any

from .env import Env

class ActionRun(ABC):
    @abstractmethod
    def run(self, env: Env, request: Dict[str, Any]) -> Dict[str, Any]:
        pass

class EnvGet:
    @staticmethod
    def read(env, name):
        value = env[name]
        if value is None:
            raise Exception(f'环境变量:{name} 不存在!')
        return value
    
class DictGet:
    @staticmethod
    def read(dict: Dict, name):
        value = dict[name]
        if value is None:
            raise Exception(f'参数:{name} 不存在!')
        return value
