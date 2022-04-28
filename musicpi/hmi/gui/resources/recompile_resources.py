from subprocess import PIPE, Popen

if __name__ == "__main__":
    p = Popen(
        "pyside2-rcc resources.qrc -o resources_rc.py".split(),
        shell=False,
        stderr=PIPE,
        stdout=PIPE,
    )
    for line in p.stderr:
        print(line)
    for line in p.stdout:
        print(line)
