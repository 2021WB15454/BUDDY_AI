class Config:
    def __init__(self):
        self.settings = {"max_context_length": 10}
    def get(self, key, default=None):
        return self.settings.get(key, default)
