class Repo:
    def __init__(self, id, url, flag, stopStage, truncated1k, truncated10k):
        self.id = id
        self.url = url
        self.flag = flag
        self.stopStage = stopStage
        self.truncated1k = truncated1k
        self.truncated10k = truncated10k