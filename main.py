import subprocess
from time import sleep

words_txt = 'words.txt'


def read_txt(arquivo):
    with open(arquivo) as f:
        for line in f:
            yield line


def save_file(file_name, identification, data):
    with open(file_name, 'a') as f:
        f.write(identification + ' -> ' + str(data) + "\n")


if __name__ == "__main__":
    for line in read_txt(words_txt):
        try:
            # print("Comand: gh search code " + line.replace('\n', '') + " --owner=Hotmart-Org")
            proc = subprocess.Popen(["gh search code " + line.replace('\n', '') + " --owner=Hotmart-Org"],
                                    stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            repos = str(out.decode("utf-8")).split('\n')
            if len(repos) > 1:
                for repo in repos:
                    if len(str(repo)) > 1:
                        print(str(repo).split(':')[0] + " => " + repo)
            sleep(10)
        except Exception as e:
            print(f"Erro: {e} -> " + line)
