import os, re, sys, time, json, base64, random, string, ctypes, getpass, threading

try:
    import requests
    import tls_client
    import datetime
    import colorama
    import pystyle
    import uuid
except ModuleNotFoundError:
    os.system("pip install requests")
    os.system("pip install tls_client")
    os.system("pip install datetime")
    os.system("pip install colorama")
    os.system("pip install pystyle")
    os.system("pip install uuid")

from pystyle import Write, System, Colors, Colorate, Center
from datetime import datetime, timezone
from colorama import Fore, Style, init
from tls_client import Session
from raducord import *

class Config:
    config = json.load(open("data/config.json"))
    threads = config['threads']

class Promos:
    promos = []

class Console:
    def title():
        while Stats.working:
            current_time = time.time()
            elapsed_time = current_time - Stats.start
            if elapsed_time != 0:
                try:
                    success_rate = round((Stats.created / (Stats.failed + Stats.created)) * 100, 2)
                except ZeroDivisionError:
                    success_rate = 0

                try:
                    cpm = round(Stats.created / (elapsed_time / 60))
                    cph = round(Stats.created / (elapsed_time / 3600))
                except ZeroDivisionError:
                    cpm, cph = 0, 0

                elapsed_days = int(elapsed_time // 86400)
                elapsed_hours = int((elapsed_time % 86400) // 3600)
                elapsed_minutes = int((elapsed_time % 3600) // 60)
                elapsed_seconds = int(elapsed_time % 60)

                ctypes.windll.kernel32.SetConsoleTitleW(f'Chess.com Discord Promo Gen ~ Created: {Stats.created} ^| Failed: {Stats.failed} ^| CPM: {cpm} / CPH: {cph} @ {success_rate}% ^| Elapsed: {elapsed_days}d {elapsed_hours}h {elapsed_minutes}m {elapsed_seconds}s ~ .gg/raducord')
            time.sleep(0.1)

class Stats:
    created = 0
    failed = 0
    start = time.time()
    working = True

class Chess:
    def __init__(self) -> None:
        self.client = requests.Session()

        with open("data/proxies.txt", "r", encoding='utf-8') as f:
            proxies = f.read().splitlines()
            self.proxy = random.choice(proxies)

        self.client.proxies = {
            "http": f"http://{self.proxy}",
            "https": f"http://{self.proxy}"
        }

    def __randomEmail__(self) -> str:
        return f"{Utils.get_full_name().lower().replace(', ', '')}{random.randint(1111111111, 999999999999999)}@gmail.com"
    
    def __randomPassword__(self) -> str:
        return f"{Utils.get_full_name().lower().replace(', ', '')}{random.randint(11111, 99999)}Radu"
    
    def __randomUsername__(self) -> str:
        return f"{Utils.get_full_name().lower().replace(', ', '')}{random.randint(11111, 99999)}"

    def __register__(self) -> None:
        try:
            email, password, username = self.__randomEmail__(), self.__randomPassword__(), self.__randomUsername__()
            
            payload = {
                "username": username,
                "password": password,
                "email": email,
                "deviceId": f"4122fa2b7d374bc3bda955d9d{random.randint(1000000, 9999999)}", # ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
                "clientId": "1bc9f2f2-4961-11ed-8971-f9a8d47c7a48",
                "onboardingType": "september2022"
            }

            headers = {
                "user-agent": "Chesscom-Android/4.6.31-googleplay (Android/9; ASUS_I005DA; es_ES; contact #android in Slack)",
                "x-client-version": "Android4.6.31",
                "accept-language": "es-ES;q=0.8, en;q=0.7",
                "content-type": "application/x-www-form-urlencoded",
                "host": "api.chess.com",
                "connection": "Keep-Alive",
                "accept-encoding": "gzip"
            }

            r = self.client.post(
                "https://api.chess.com/v1/users?signed=Android4.6.31",
                headers=headers,
                data=payload
            )

            if r.status_code != 200:
                if "Resource not found." in r.text:
                    Logger.failed(f"Failed Registering,{email},{password}")
                    time.sleep(2)
                    Stats.failed += 1
                    self.__register__()

            Logger.success(f"Successfully Registered,{email},{password}")
            with open("results/accounts.txt", "a+", encoding="utf-8") as f:
                f.write(f"{email}:{password}\n")
        
            user_uuid = r.json()['data']['uuid'] # r.json()['data']['oauth']['access_token']
            return user_uuid, email
        except Exception as e:
            Logger.custom("c1121f", "!", f"ERROR,{e},Exception")
    
    def __fetchPromoCode__(self) -> None:
        try:
            user_uuid, email = self.__register__()

            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'es-ES;q=0.8, en;q=0.7',
                'content-type': 'application/json',
                'origin': 'https://www.chess.com',
                'priority': 'u=1, i',
                'referer': 'https://www.chess.com/play/computer/discord-wumpus?utm_source=chesscom&utm_medium=homepagebanner&utm_campaign=discord2024',
                'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            }

            payload = {
                'userUuid': user_uuid,
                'campaignId': '4daf403e-66eb-11ef-96ab-ad0a069940ce',
            }

            while True:
                r = self.client.post(
                    'https://www.chess.com/rpc/chesscom.partnership_offer_codes.v1.PartnershipOfferCodesService/RetrieveOfferCode',
                    headers=headers,
                    json=payload,
                )

                promo = r.json()['codeValue']

                if promo not in Promos.promos:
                    Promos.promos.append(promo)
                    Logger.info(f"Fetched Promo Code,{email},{promo}")
                    Logger.captcha(f"Successfully Saved Promo,{promo},results/promos.txt")
                    with open("results/promos.txt", "a+", encoding="utf-8") as f:
                        f.write(f"https://discord.com/billing/promotions/{promo}" + "\n")
                    
                    Stats.created += 1
                    break
                else:
                    time.sleep(1)

        except Exception as e:
            Logger.custom("c1121f", "!", f"ERROR,{e},Exception")

if __name__ == "__main__":
    try:  
        text = TextUtils.make_ascii("Discord\nPromo\nGenerator", font="bulbhead")
        centered_text = "\n".join(line.center(120) for line in text.split("\n"))
        banner = BannerUtils.lines_4(TextUtils.strikethrough_text("By H4cK3dR4Du"))
        centered_banner = '\n'.join(' ' * ((120 - max(len(line) for line in banner.split('\n'))) // 2) + line for line in banner.split('\n'))
        print(Gradient.gradient_text(centered_text + f"\n\n{centered_banner}", GradientColors.purple_to_red))

        threading.Thread(target=Console.title).start()
        while True:
            while threading.active_count() - 1 < Config.threads:
                chess = Chess()
                threading.Thread(target=chess.__fetchPromoCode__).start()
            time.sleep(1)
    except:
        pass