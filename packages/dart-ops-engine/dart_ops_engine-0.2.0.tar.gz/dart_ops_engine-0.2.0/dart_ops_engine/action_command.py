import json
from .env import Env
from .execute import Execute
from .action_run import ActionRun
import os


class ActionCommand:
    def __init__(self, name, description,request_args: dict, action_run: ActionRun):
        self.name = name
        self.description = description
        self.action_run = action_run
        self.request_args = request_args
    

    def run(self, args):
        id = args.id
        index = str(args.index)
        execute = Execute.cache(id) if id else None
        data = Execute.get_request_data(id)
        self.request_args.update({str(k): str(v) for k, v in data.items()})
        if execute:
            execute.save_request_data(data, index)

        response = self.action_run.run(execute.memory_env if execute else Env(os.environ), self.request_args)
        if execute:
            execute.save_response_data(response, index)
        else:
            print(json.dumps(response))
    