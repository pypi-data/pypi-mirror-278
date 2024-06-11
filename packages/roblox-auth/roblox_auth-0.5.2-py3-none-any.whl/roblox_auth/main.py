from logging import Manager
import os
from pickle import GET
import subprocess
import platform
import requests
import threading
import re
import glob
import time
from urllib.parse import quote
import random
from datetime import datetime
import math

from webdriver import get_cookie

class AccountLaunch:
    def __init__(self, cookie: str, placeId: int, VIP: bool = False, privateServerLink: str = "") -> None:
        self.cookie = cookie
        self.placeId = placeId
        self.VIP = VIP
        self.privateServerLink = privateServerLink

    # get x-csrf-token
    def get_xsrf(self):
        auth_url = "https://auth.roblox.com/v2/logout"
        xsrf_request = requests.post(auth_url, cookies={'.ROBLOSECURITY': self.cookie})
        return xsrf_request.headers["x-csrf-token"]

    # opens a ticket to join a server
    def get_authentication_ticket(self):
        launch_url = 'https://auth.roblox.com/v1/authentication-ticket/'
        response = requests.post(launch_url, headers={'X-CSRF-Token': self.get_xsrf(), "Referer": "https://www.roblox.com/games/4924922222/Brookhaven-RP"}, cookies={'.ROBLOSECURITY': self.cookie})
        ticket = response.headers.get("rbx-authentication-ticket", "")
        return ticket

    # gets server id
    def job_id(self):
        try:
            response = requests.get(f"https://games.roblox.com/v1/games/{self.placeId}/servers/0?sortOrder=1&excludeFullGames=true&limit=25").json()
            data = response["data"][7]
            return data["id"]
        except KeyError:
            response = requests.get(f"https://games.roblox.com/v1/games/{self.placeId}/servers/0?sortOrder=1&excludeFullGames=true&limit=25").json()
            data = response["data"][4]
            return data["id"]
    
    def get_link_code(self):
        url = self.privateServerLink

        link_code_match = re.search(r'privateServerLinkCode=(\d+)', url)

        LinkCode = link_code_match.group(1) if link_code_match else ''
        return LinkCode
    
    def GetVersion(self):
        new_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Roblox\\Versions"

        all_dirs = [d for d in glob.glob(new_path + "\\*") if os.path.isdir(d) and "version-" in os.path.basename(d)]

        if not all_dirs:
            raise FileNotFoundError("No directories containing 'version-' found")

        latest_dir = max(all_dirs, key=os.path.getctime)
        return latest_dir
    
    def AddLogin(self, File: bool = True):
        cookie = get_cookie(File=File)
        return cookie
    
    # launch roblox function opens roblox with the inserted roblox cookie
    def launch_roblox(self):
        roblox_executable_path = None
        current_version = self.GetVersion()
        r_path = os.path.join(current_version)

        launch_time = math.floor((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds() * 1000)
        browser_tracker_id = str(random.randint(100000, 175000)) + str(random.randint(100000, 900000))

        if not os.path.exists(r_path):
            return "ERROR: Failed to find ROBLOX executable"

        roblox_executable_path = os.path.join(r_path, "RobloxPlayerBeta.exe")
        
        print(roblox_executable_path)

        launch_url = ""
        if self.VIP:
            launch_url = f"https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestPrivateGame&placeId={self.placeId}&linkCode={self.get_link_code()}" # &accessCode={self.privateServerLink}
        else:
            launch_url = f"https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestGame&placeId={self.placeId}{'' if not self.job_id() else '&gameId=' + self.job_id()}&isPlayTogetherGame=false{'&isTeleport=true'}"
        
        encoded_url = quote(launch_url)
        arguments = f'roblox-player:1+launchmode:play+gameinfo:{self.get_authentication_ticket()}+launchtime:{launch_time}+placelauncherurl:{encoded_url}+browsertrackerid:{browser_tracker_id}+robloxLocale:en_us+gameLocale:en_us+channel:+LaunchExp:InApp'

        if platform.system() == "Windows":
            subprocess.Popen([roblox_executable_path, arguments])
        
        return "Success"



# can launch multiple roblox accounts.
def multi_roblox():
    def roblox_m():
        import win32event
        mutex_name = "ROBLOX_singletonMutex"
        mutex = win32event.CreateMutex(None, 1, mutex_name)

        done, oof = 9e9, 0
        while done > oof:
            pass

        win32event.ReleaseMutex(mutex)

    # Start multi roblox silently
    Multi_thread = threading.Thread(target=roblox_m)
    Multi_thread.start()
    return True

# Launch account premade function
def launch_account(cookie: str, placeId: int, VIP: bool = False, privateServerLink: str = ""):
    privateServerLink = privateServerLink or ""

    Manager = AccountLaunch(cookie, placeId, VIP, privateServerLink)

    Manager.launch_roblox()

    # Account_thread = threading.Thread(target=Manager.launch_roblox)
    # Account_thread.start()
    
    return True



