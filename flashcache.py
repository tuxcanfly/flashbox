import os
import subprocess

def get_pids():
    pids = []

    cat = subprocess.Popen(['ps', 'aux'],
                            stdout=subprocess.PIPE,
                            )

    grep = subprocess.Popen(['grep', 'libflashplayer.so'],
                            stdin=cat.stdout,
                            stdout=subprocess.PIPE,
                            )

    tr = subprocess.Popen(['tr', '-s', ' '],
                            stdin=grep.stdout,
                            stdout=subprocess.PIPE,
                            )

    cut = subprocess.Popen(['cut', '-d', ' ', '-f', '2'],
                            stdin=tr.stdout,
                            stdout=subprocess.PIPE,
                            )

    end_of_pipe = cut.stdout

    for line in end_of_pipe:
        pids.append(line.strip())
    return pids

def get_file_names(pid):
    file_names = []

    path = '/proc/%s/fd/' % (pid)

    if os.path.exists(path):

        ls = subprocess.Popen(['ls', '-l', path],
                                stdout=subprocess.PIPE,
                                )

        grep = subprocess.Popen(['grep', 'FlashXX'],
                                stdin=ls.stdout,
                                stdout=subprocess.PIPE,
                                )

        tr = subprocess.Popen(['tr', '-s', ' '],
                                stdin=grep.stdout,
                                stdout=subprocess.PIPE,
                                )

        cut = subprocess.Popen(['cut', '-d', ' ', '-f', '9'],
                                stdin=tr.stdout,
                                stdout=subprocess.PIPE,
                                )

        end_of_pipe = cut.stdout

        for line in end_of_pipe:
            file_names.append(line.strip())

    return file_names

if __name__ == '__main__':
    for pid in get_pids():
        print get_file_names(pid)
