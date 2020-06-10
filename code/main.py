import os
import json
import time
import subprocess

    
def main():
    azure_credentials = os.environ.get("INPUT_AZURE_CREDENTIALS", default="{}")
    command='az login --service-principal --username "ab96606e-49a7-45d3-a575-5172e11fdb7f" --password "^s:e6b4uCMXxN168t+i?[f](\\`E~8YeAP" --tenant "2d1aba9c-5938-402b-90b9-72a284a4bced"'
    try:
        app_create = subprocess.check_output(command, shell=True)
        print(app_create)
    except Exception as ex:
        print(ex) 

if __name__ == "__main__":
    main()
