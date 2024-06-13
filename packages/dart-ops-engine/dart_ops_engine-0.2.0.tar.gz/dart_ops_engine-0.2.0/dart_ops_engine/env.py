class Env:
    def __init__(self, environment=None):
        self.env = environment or {}

    def __setitem__(self, name, value):
        self.env[name] = value

    def __getitem__(self, name):
        return self.env.get(name)

    def __add__(self, environment):
        self.env.update(environment.env)

