from git import Commit as GitCommit, Repo as GitRepo
from gitdb.util import to_bin_sha

def getDataForCommit(self, commit: GitCommit, repoUrl: str, clonedRepo: GitRepo) -> object:
        commitUrl = f"{repoUrl}/commits/{commit.hexsha}"
        commitFiles = []

        # get the files that were added or modified in the commit
        if len(commit.parents) == 0:
            # get the format of an empty tree
            format = clonedRepo.git.rev_parse("--show-object-format")
            if format == "sha1":
                previousCommit = GitCommit(clonedRepo, to_bin_sha('4b825dc642cb6eb9a060e54bf8d69288fbee4904'))
            else:
                raise Exception(f"The initial commit uses a different format than sha1({format})")
            
            # compare the first commit to the empty tree
            for diff in previousCommit.diff(commit):
                if diff.b_path.endswith('.yaml') or diff.b_path.endswith('.yml'):
                    if diff.change_type == 'A':
                        commitFiles.append(diff.b_path)
        else:
            previousCommit = commit.parents[0]
            # compare the commit to the previous one
            for diff in previousCommit.diff(commit):
                if diff.b_path.endswith('.yaml') or diff.b_path.endswith('.yml'):
                    if diff.change_type == 'A' or diff.change_type == 'M':
                        commitFiles.append(diff.b_path)
        return {
            'commit_url': commitUrl,
            'commit_hash': commit.hexsha,
            'message': commit.message,
            'filePaths': commitFiles
        }