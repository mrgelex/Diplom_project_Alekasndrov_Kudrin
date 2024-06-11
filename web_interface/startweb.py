import subprocess
def startweb():
    subprocess.run(['python', 'web_interface/manage.py', 'runserver'])
if __name__ == '__main__':
    startweb()