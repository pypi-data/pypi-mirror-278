import os

class CacheManager:
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir

    @property
    def execute_dir(self):
        return os.path.join(self.cache_dir, 'execute')

    def env_file_path(self, execute):
        return os.path.join(self.execute_dir, str(execute.id), '.env')

    def action_request_file_path(self, execute, action_id):
        return os.path.join(self.execute_dir, str(execute.id), action_id, 'request.json')

    def action_response_file_path(self, execute, action_id):
        return os.path.join(self.execute_dir, str(execute.id), action_id, 'response.json')

    def config_file_path(self, execute):
        return os.path.join(self.execute_dir, str(execute.id), 'config.json')
