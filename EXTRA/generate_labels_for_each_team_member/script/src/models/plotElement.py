class PlotElement:
    def __init__(self, commitId: int, url: str):
        self.commitId = commitId
        self.url = url,
        self.message = None
        self.awareness = False
        self.increase = False
        self.save = False
        self.alert = False
        self.change = False
        self.test = False
        self.area = False
        self.billing_mode = False
        self.cluster = False
        self.cpu = False
        self.domain = False
        self.feature = False
        self.instance = False
        self.nat = False
        self.networking = False
        self.policy = False
        self.provider = False
        self.ram = False
        self.storage = False
        self.vpn = False
        self.logging = False
        self.permissions = False
        self.unrelated = False
    
    def getResult(self):
        return (self.unrelated, self.awareness, self.increase, self.save, self.alert, self.change, self.test, self.area, self.billing_mode, self.cluster, self.cpu, self.domain, self.feature, self.instance, self.nat, self.networking, self.policy, self.provider, self.ram, self.storage, self.vpn, self.logging, self.permissions)

    def getListOfTrueLabels(self):
        return [key for key, value in self.__dict__.items() if value == True]
    
    def toDict(self):
        return {
            "commitId": self.commitId,
            "type": "commit",
            "url": self.url[0],
            "content": {
                "message": self.message,
            },
            "codes": self.getListOfTrueLabels()
        }