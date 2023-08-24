import subprocess
from decouple import config
from time import sleep

INPUT_TXT = config('INPUT_TXT')
OWNER_REPO_GIT = config('OWNER_REPO_GIT')


def read_txt(file):
    with open(file) as f:
        for lineFile in f:
            yield lineFile


def save_file(file_name, identification, data):
    with open(file_name, 'a') as f:
        f.write(identification + ' -> ' + str(data) + "\n")


if __name__ == "__main__":
    # os.system("gh auth login")
    foundRepos = []
    for line in read_txt(INPUT_TXT):
        try:
            query = line.replace('\n', '')
            proc = subprocess.Popen([f"gh search code {query} --owner={OWNER_REPO_GIT}"],
                                    stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            repos = str(out.decode("utf-8")).split('\n')
            if len(repos) > 1:
                for repo in repos:
                    if len(str(repo)) > 1:
                        # print(repo)
                        filtered = list(filter(lambda _obj: _obj['repo'] == str(repo).split(':')[0]
                                                            and _obj['query'] == query, foundRepos))
                        if len(filtered) > 0:
                            filtered[0]['fileName'].append(str(repo).split(':')[1])
                        else:
                            obj = {
                                'query': query,
                                'repo': str(repo).split(':')[0],
                                'fileName': [str(repo).split(':')[1]]
                            }
                            foundRepos.append(obj)
            sleep(5)
        except Exception as e:
            print(f"Error: {e} -> " + line)
    print('-------------------------------------------')
    for repo in foundRepos:
        print("Query = " + repo['query'])
        print("=> " + repo['repo'])
        for file in repo['fileName']:
            print("     => " + file)
        print('-------------------------------------------')
