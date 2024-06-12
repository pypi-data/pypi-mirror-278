import os
import subprocess

def install_pip():
    try:
        subprocess.check_output('dpkg -s python3-pip', shell=True)
    except subprocess.CalledProcessError:
        subprocess.check_output('sudo apt update', shell=True)
        subprocess.check_output('sudo apt install python3-pip -y', shell=True)

def install_requests():
    try:
        import requests
    except ImportError:
        os.system('pip3 install requests')
        os.system('pip3 install requests[socks]')

def install_tor():
    try:
        subprocess.check_output('which tor', shell=True)
    except subprocess.CalledProcessError:
        subprocess.check_output('sudo apt update', shell=True)
        subprocess.check_output('sudo apt install tor -y', shell=True)
