# __init__.py

# Import Version
from .version import __version__

# Import Other Modules
from .econkit import econometrics, finance

# Version Check and Update Function
import subprocess
import sys
import requests
from distutils.version import LooseVersion

def check_for_latest_version():
    try:
        current_version = __version__
        response = requests.get('https://pypi.org/pypi/econkit/json')
        latest_version = response.json()['info']['version']
        
        if LooseVersion(current_version) < LooseVersion(latest_version):
            print(f"A new version of econkit is available: {latest_version}")
            update = input("Do you want to update now? (yes/no): ").strip().lower()
            if update == 'yes':
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "econkit"])
                print("Library updated. Please restart your application.")
    except Exception as e:
        print(f"Error checking for library update: {e}")

# Initialize the version check at the end of the file
check_for_latest_version()
