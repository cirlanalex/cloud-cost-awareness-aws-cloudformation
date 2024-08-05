class Commit():
    def __init__(self, id, repoId, url, hash, keywords, hasNonTemplate):
        self.id = id
        self.repoId = repoId
        self.url = url
        self.hash = hash
        self.keywords = keywords
        self.hasNonTemplate = hasNonTemplate