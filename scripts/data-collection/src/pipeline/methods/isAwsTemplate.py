def isAwsFileTemplate(self, fileContent: str) -> bool:
        for template in self.templates:
            if fileContent == template:
                return True
        return False