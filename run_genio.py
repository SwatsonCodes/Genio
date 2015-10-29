import subprocess

servers = [subprocess.Popen(['python', './api_server.py']), subprocess.Popen(['python', './ui/ui_server.py'])]
for s in servers:
    s.wait()
