import os, re, sys, time, json, html, base64, random, string, ctypes, getpass, threading

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
from bs4 import BeautifulSoup
from raducord import *

class Config:
    config = json.load(open("data/config.json"))
    threads = config['threads']

class Promos:
    promos = []

class RaduLogger:
    def __init__(self, text) -> None:
        self.text = text

    def __success__(self) -> None:
        print(f'{ColorUtils.hex_color("#FFFFFF")} [{ColorUtils.hex_color("#6c757d")} {Utils.log_time()} {ColorUtils.hex_color("#FFFFFF")}] {ColorUtils.hex_color("#6c757d")}| {ColorUtils.hex_color("#29bf12")}SUC {ColorUtils.hex_color("#6c757d")}| {self.text}')

    def __failed__(self) -> None:
        print(f'{ColorUtils.hex_color("#FFFFFF")} [{ColorUtils.hex_color("#6c757d")} {Utils.log_time()} {ColorUtils.hex_color("#FFFFFF")}] {ColorUtils.hex_color("#6c757d")}| {ColorUtils.hex_color("#d00000")}ERR {ColorUtils.hex_color("#6c757d")}| {self.text}')

    def __info__(self) -> None:
        print(f'{ColorUtils.hex_color("#FFFFFF")} [{ColorUtils.hex_color("#6c757d")} {Utils.log_time()} {ColorUtils.hex_color("#FFFFFF")}] {ColorUtils.hex_color("#6c757d")}| {ColorUtils.hex_color("#2a9d8f")}INF {ColorUtils.hex_color("#6c757d")}| {self.text}')
    
    def __warning__(self) -> None:
        print(f'{ColorUtils.hex_color("#FFFFFF")} [{ColorUtils.hex_color("#6c757d")} {Utils.log_time()} {ColorUtils.hex_color("#FFFFFF")}] {ColorUtils.hex_color("#6c757d")}| {ColorUtils.hex_color("#ffea00")}WAR {ColorUtils.hex_color("#6c757d")}| {self.text}')

    def __debugInfo__(self) -> None:
        print(f'{ColorUtils.hex_color("#FFFFFF")} [{ColorUtils.hex_color("#6c757d")} {Utils.log_time()} {ColorUtils.hex_color("#FFFFFF")}] {ColorUtils.hex_color("#6c757d")}| {ColorUtils.hex_color("#ff7b00")}DBG {ColorUtils.hex_color("#6c757d")}| {self.text}')

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
        self.client = tls_client.Session(
            client_identifier="chrome_126",
            # ja3_string=self.__fetchJA3__(),
            random_tls_extension_order=True
        )

        with open("data/proxies.txt", "r", encoding='utf-8') as f:
            proxies = f.read().splitlines()
            self.proxy = random.choice(proxies)

        self.client.proxies = {
            "http": f"http://{self.proxy}",
            "https": f"http://{self.proxy}"
        }

        self.client.headers = {
            'accept': '*/*',
            'accept-language': 'es-ES;q=0.8, en;q=0.7',
            'cache-control': 'no-cache',
            'origin': 'https://www.chess.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }

    def __fetchJA3__(self) -> str:
        client = tls_client.Session(
            client_identifier='chrome_126',
            random_tls_extension_order=True
        )

        try:
            response = client.get('https://tls.peet.ws/api/clean')
        except:
            return self.__fetchJA3__()
        
        if response.status_code == 200:
            return response.json().get('ja3')
        else:
            return None

    def __randomEmail__(self) -> str:
        return f"h4_{Utils.get_full_name().lower().replace(', ', '_')}{random.randint(1111111111, 999999999999999)}@gmail.com"

    def __randomPassword__(self) -> str:
        return f"{Utils.get_full_name().lower().replace(', ', '')}{random.randint(100000, 9999999)}R$"
    
    def __randomUsername__(self) -> str:
        return f"{Utils.get_full_name().lower().replace(', ', '')}{random.randint(100000, 9999999)}"

    def __register__(self) -> None:
        try:
            email, password, username = self.__randomEmail__(), self.__randomPassword__(), self.__randomUsername__()
            
            register_page = self.client.get("https://www.chess.com/register")
            self.client.headers['referer'] = "https://www.chess.com/register"
            json_data = BeautifulSoup(register_page.text, "html.parser").find('div', attrs={'id': 'registration'})['data-form-params']
            token = json.loads(html.unescape(json_data))['token']['value']
            session_id = self.client.get("https://ssl.kaptcha.com/collect/sdk", params={'m': '850100'}).text.split('ka.sessionId=')[1].split("'")[1]
            
            data = {
                'registration[skillLevel]': 1,
                'registration[email]': email,
                'registration[password]': password,
                # 'registration[turnstile_token]': Cloudfare.__getTurnstile__(self), # cf it's sooooo fucking easy, reverse yourself 🥱🥱
                'registration[timezone]': 'Europe/Madrid',
                'registration[_token]': token,
                'kountSessionId': session_id,
                'fingerprint': ''.join(random.choices(string.ascii_lowercase + string.digits, k=32)),
                'registration[friend]': '',
                'registration[username]': username,
                'registration[opt_in]': 'on'
            }
            
            r = self.client.post('https://www.chess.com/register', data=data, allow_redirects=True)

            try:
                user_uuid = r.text.split("user=")[1].split("&")[0]
            except (KeyError, IndexError):
                RaduLogger(f"{ColorUtils.hex_color('#d00000')}Failed to register: {ColorUtils.hex_color('#bc4b51')}{email}").__failed__()
                time.sleep(2)
                Stats.failed += 1
                self.__register__()

            RaduLogger(f"{ColorUtils.hex_color('#29bf12')}Registered: {ColorUtils.hex_color('#bc4b51')}{email}").__success__()

            with open("results/accounts.txt", "a+", encoding="utf-8") as f:
                f.write(f"{email}:{password}\n")

            return user_uuid, email
        except Exception as e:
            # Logger.custom("c1121f", "!", f"ERROR,{e},Exception")
            pass
    
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
                    RaduLogger(f"{ColorUtils.hex_color('#aacc00')}Got promocode: {ColorUtils.hex_color('#bc4b51')}{promo} {ColorUtils.hex_color('#FFFFFF')}({ColorUtils.hex_color('#3d405b')}{email}{ColorUtils.hex_color('#FFFFFF')})").__info__()
                    with open("results/promos.txt", "a+", encoding="utf-8") as f:
                        f.write(f"https://discord.com/billing/promotions/{promo}" + "\n")
                    
                    Stats.created += 1
                    break
                else:
                    time.sleep(1)

            self.__fetchPromoCode__()
        except Exception as e:
            # Logger.custom("c1121f", "!", f"ERROR,{e},Exception")
            pass

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