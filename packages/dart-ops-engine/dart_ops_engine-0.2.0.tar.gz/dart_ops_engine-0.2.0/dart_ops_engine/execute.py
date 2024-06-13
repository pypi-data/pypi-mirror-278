import json
import os
import time

from .cache_manager import CacheManager
from .env import Env

from .define import engine_dir, request_argument

class Execute:
    def __init__(self, id=None, use_cache=False, configs=None):
        self.id = id or int(time.time() * 1000)
        self.use_cache = use_cache
        self.configs = configs or []
        self.cache_manager = CacheManager(cache_dir=os.path.join(engine_dir, 'execute'))
        self.memory_env = Env(environment=os.environ)
        self.configs = configs
    
    def init(self):
        self.memory_env += self._load_env()

    def _load_env(self):
        env_file_path = self.cache_manager.env_file_path(self)
        if not os.path.exists(env_file_path):
            return Env(environment={})
        with open(env_file_path, 'r') as file:
            env_contents = file.readlines()
        env_map = {}
        for content in env_contents:
            key, value = content.strip().split('=')
            env_map[key] = value
        return Env(environment=env_map)
    @classmethod
    def cache(self, id):
        return self(id=id, use_cache=True)

    def save_request_data(self,data, action_id):
        path = self.cache_manager.action_request_file_path(self, action_id)
        self.save_json_from_path(path, data)
    def save_response_data(self, data, action_id):
        path = self.cache_manager.action_response_file_path(self, action_id)
        self.save_json_from_path(path, data)
    def save_json_from_path(self,path, data):
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as file:
            json.dump(data, file)
    @staticmethod
    def get_request_data(id):
        data = {}
        execute = None
        if id is not None:
            execute = Execute.cache(id)
            execute.init()

        for arg in request_argument:
            if arg.startswith('--args='):
                # --args=name=value
                values = arg[7:].split('=')
                data[values[0]] = values[1]
            elif arg.startswith('--env=') and execute is not None:
                # --env=name
                name = arg[6:]
                value = execute.memory_env.env.get(name)
                if value is not None:
                    data[name] = value
            elif arg.startswith('--res=') and execute is not None:
                # --res=a|index|name,1,2,3
                arg_name = execute.key(arg)
                value = execute.rep_value(arg)
                if value is not None and arg_name is not None:
                    data[arg_name] = value
            elif arg.startswith('--req=') and execute is not None:
                # --req=a|index|name,1,2,3
                arg_name = execute.key(arg)
                value = execute.req_value(arg)
                if value is not None and arg_name is not None:
                    data[arg_name] = value

        return data
