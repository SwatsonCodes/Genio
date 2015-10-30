import subprocess
import sys

if __name__ == '__main__':
    pyname = 'python'
    if sys.version_info[0] < 3:
        pyname += '3'

    servers = [subprocess.Popen([pyname, './api_server.py']), subprocess.Popen([pyname, './ui/ui_server.py'])]
    for s in servers:
        s.wait()
