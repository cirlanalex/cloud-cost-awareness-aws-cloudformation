from models.repo import Repo

def checkCommitForKeywords(self, commit: object, repo: Repo):
        keywords = []
        keywordsFound = False
        for keyword in self.keywords:
            if keyword[1] in commit['message'].lower():
                keywords.append(keyword[0])
                keywordsFound = True
        if keywordsFound:
            commit['keywords'] = keywords
            self.checkCommitForAws(commit, repo)