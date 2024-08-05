from subprocess import Popen, DEVNULL

def checkoutCommitFiles(self, commit: object):
        try:
            with open(f"temp_repo/.git/info/sparse-checkout", "w") as file:
                pass

            # add the files to the sparse-checkout file
            for filePath in commit['filePaths']:
                with open(f"temp_repo/.git/info/sparse-checkout", "a") as file:
                    file.write(f"{filePath}\n")
            
            # checkout the commit
            process = Popen(["git", "-C", "temp_repo", "checkout", commit['commit_hash']], stdout=DEVNULL, stderr=DEVNULL)
            process.wait()
        except Exception:
            raise