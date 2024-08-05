class PlotElement:
    def __init__(self, commitId: int):
        self.commitId = commitId
        self.awareness = False
        self.increase = False
        self.save = False
        self.change = False
        self.test = False
        self.track = False
        self.alert = False
        self.area = False
        self.billing_mode = False
        self.cluster = False
        self.cpu = False
        self.domain = False
        self.feature = False
        self.instance = False
        self.logging = False
        self.nat = False
        self.networking = False
        self.policy = False
        self.provider = False
        self.ram = False
        self.report = False
        self.service = False
        self.storage = False
        self.vpn = False
    
    def getResult(self):
        return (self.awareness, self.increase, self.save, self.change, self.test, self.track, self.alert, self.area, self.billing_mode, self.cluster, self.cpu, self.domain, self.feature, self.instance, self.logging, self.nat, self.networking, self.policy, self.provider, self.ram, self.report, self.service, self.storage, self.vpn)

    def getCommonResult(self):
        return (self.awareness, self.increase, self.save, self.alert, self.area, self.billing_mode, self.cluster, self.domain, self.feature, self.instance, self.networking, self.policy, self.provider, self.storage)