try:
    import os
    import requests
    from user_agent import generate_user_agent
    from hashlib import md5
    import random
    from bs4 import BeautifulSoup
    import pycountry
    import time    
    from mnemonic import Mnemonic
    from secrets import token_hex
    from datetime import datetime
    from uuid import uuid4
except:
    os.system("pip install requests user_agent bs4 pycountry uuid mnemonic")
    import os
    import requests
    from user_agent import generate_user_agent
    from hashlib import md5
    import random
    from bs4 import BeautifulSoup
    import pycountry
    import time
    from datetime import datetime
    from secrets import token_hex
    from uuid import uuid4
    from mnemonic import Mnemonic
    
class Instagram:
    @staticmethod
    def CheckInsta(email):
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/accounts/signup/email/',
            'user-agent': generate_user_agent(),
            'x-csrftoken': md5(str(time.time()).encode()).hexdigest()
        }
        data = {
            'email': email,
        }
        response = requests.post('https://www.instagram.com/api/v1/web/accounts/check_email/', headers=headers, data=data)
        if 'email_is_taken' in str(response.text):
            return {'status': 'ok', 'Is_Available': 'true', 'AHMED': '@maho_s9'}
        else:
            return {'status': 'bad', 'Is_Available': 'false', 'AHMED': '@maho_s9'}

class TikTok:
    @staticmethod
    def CheckTik(email):
        try:
            ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
            pl = [19, 20, 21, 22, 23, 24, 25, 80, 53, 111, 110, 443, 8080, 139, 445, 512, 513, 514, 4444, 2049, 1524, 3306, 5900]
            port = random.choice(pl)
            proxy = ip + ":" + str(port)
            url = "https://www.tiktok.com/passport/web/user/check_email_registered?shark_extra=%7B%22aid%22%3A1459%2C%22app_name%22%3A%22Tik_Tok_Login%22%2C%22app_language%22%3A%22en%22%2C%22device_platform%22%3A%22web_mobile%22%2C%22region%22%3A%22SA%22%2C%22os%22%3A%22ios%22%2C%22referer%22%3A%22https%3A%2F%2Fwww.tiktok.com%2Fprofile%22%2C%22root_referer%22%3A%22https%3A%2F%2Fwww.google.com%22%2C%22cookie_enabled%22%3Atrue%2C%22screen_width%22%3A390%2C%22screen_height%22%3A844%2C%22browser_language%22%3A%22en-us%22%2C%22browser_platform%22%3A%22iPhone%22%2C%22browser_name%22%3A%22Mozilla%22%2C%22browser_version%22%3A%225.0%20%28iPhone%3B%20CPU%20iPhone%20OS%2014_4%20like%20Mac%20OS%20X%29%20AppleWebKit%2F605.1.15%20%28KHTML%2C%20like%20Gecko%29%20Version%2F14.0.3%20Mobile%2F15E148%20Safari%2F604.1%22%2C%22browser_online%22%3Atrue%2C%22timezone_name%22%3A%22Asia%2FRiyadh%22%2C%22is_page_visible%22%3Atrue%2C%22focus_state%22%3Atrue%2C%22is_fullscreen%22%3Afalse%2C%22history_len%22%3A17%2C%22battery_info%22%3A%7B%7D%7D&msToken=vPgBDLGXZNEf56bl_V4J6muu5nAYCQi5dA6zj49IuWrw2DwDUZELsX2wz2_2ZYtzkbUF9UyblyjQTsIDI5cclvJQ6sZA-lHqzKS1gLIJD9M6LDBgII0nxKqCfwwVstZxhpppXA==&X-Bogus=DFSzsIVLC8A-dJf6SXgssmuyRsO1&_signature=_02B4Z6wo00001dTdX3QAAIDBDn9.7WbolA3U3FvAABfU8c"
            data = f"email={email}&aid=1459&language=en&account_sdk_source=web&region=SA"
            headers = {
                "User-Agent": generate_user_agent(),
            }
            response = requests.post(url, headers=headers, data=data, proxies={'http': proxy})
            if '"data":{"is_registered":1},"message":"success"' in response.text:
                return {'status': 'ok', 'Is_Available': 'true', 'AHMED': '@maho_s9'}
            elif '{"data":{"is_registered":0},"message":"success"}' in response.text:
            	return {'status': 'ok', 'Is_Available': 'false', 'AHMED': '@maho_s9'}
            else:
                return {'status': 'bad', 'resposne': 'TurnVPN....!', 'AHMED': '@maho_s9'}
        except:
            return {'status': 'Sorry Error Proxy', 'AHMED': '@maho_s9'}

class BIN:
    @staticmethod
    def Process_Bin(P):
        try:
            start_time = time.time()
            meet_headers = {
                'Referer': 'https://bincheck.io/ar',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            }

            response = requests.get(f'https://bincheck.io/ar/details/{P[:6]}', headers=meet_headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            table1 = soup.find('table', class_='w-full table-auto')
            rows1 = table1.find_all('tr')

            table2 = soup.find_all('table', class_='w-full table-auto')[1]
            rows2 = table2.find_all('tr')

            bin_, brand, card_type, card_level, bank, bank_phone = "", "", "", "", "", ""
            country_name, country_iso_a2, country_iso_a3, country_flag, currency = "", "", "", "", ""

            for row in rows1:
                cells = row.find_all('td')
                if len(cells) == 2:
                    cell1_text = cells[0].text.strip()
                    cell2_text = cells[1].text.strip()
                    if cell1_text == 'BIN/IIN':
                        bin_ = cell2_text
                    elif cell1_text == 'العلامة التجارية للبطاقة':
                        brand = cell2_text
                    elif cell1_text == 'نوع البطاقة':
                        card_type = cell2_text
                    elif cell1_text == 'تصنيف البطاقة':
                        card_level = cell2_text
                    elif cell1_text == 'اسم المصدر / البنك':
                        bank = cell2_text
                    elif cell1_text == 'المُصدِر / هاتف البنك':
                        bank_phone = cell2_text

            for row in rows2:
                cells = row.find_all('td')
                if len(cells) == 2:
                    cell1_text = cells[0].text.strip()
                    cell2_text = cells[1].text.strip()
                    if cell1_text == 'اسم الدولة ISO':
                        country_name = cells[1].text.strip()
                    elif cell1_text == 'رمز البلد ISO A2':
                        country_iso_a2 = cell2_text
                    elif cell1_text == 'ISO كود الدولة A3':
                        country_iso_a3 = cell2_text
                    elif cell1_text == 'علم الدولة':
                        country_flag = cells[1].find('img')['src']
                    elif cell1_text == 'عملة البلد ISO':
                        currency = cell2_text

            try:
                country = pycountry.countries.get(name=country_name)
                flag = country.flag if country else ""
            except:
                flag = ""

            end_time = time.time()
            duration = int(end_time - start_time)

            msg = {
                "BIN": bin_,
                "Info": f"{card_type} - {brand} - {card_level}",
                "Issuer": bank,
                "Country": f"{country_name} {flag}",
                "Phone": bank_phone,
                "Other": f"{currency} - {country_iso_a2} - {country_iso_a3}",
                "Time": f"{duration}s",
                "status": "ok",
                "By": "@maho_s9"
            }
            return msg
        except:
            return {'status': 'Sorry Error', 'AHMED': '@maho_s9'}
            
class InfoIG:
    @staticmethod
    def Instagram_Info(user):
        try:
            ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
            pl = [19, 20, 21, 22, 23, 24, 25, 80, 53, 111, 110, 443, 8080, 139, 445, 512, 513, 514, 4444, 2049, 1524, 3306, 5900]
            port = random.choice(pl)
            proxy = ip + ":" + str(port)
            uid = uuid4().hex.upper()
            csr = token_hex(8) * 2
            miid = token_hex(13).upper()
            dtr = token_hex(13)
            headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'ar,en;q=0.9',
                'cookie': f'ig_did={uid}; datr={dtr}; mid={miid}; ig_nrcb=1; csrftoken={csr}; ds_user_id=56985317140; dpr=1.25',
                'referer': f'https://www.instagram.com/{user}/?hl=ar',
                'sec-ch-prefers-color-scheme': 'dark',
                'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
                'sec-ch-ua-full-version-list': '"Chromium";v="112.0.5615.138", "Google Chrome";v="112.0.5615.138", "Not:A-Brand";v="99.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': generate_user_agent(),
                'viewport-width': '1051',
                'x-asbd-id': '198387',
                'x-csrftoken': str(csr),
                'x-ig-app-id': '936619743392459',
                'x-ig-www-claim': '0',
                'x-requested-with': 'XMLHttpRequest',
            }
            rr = requests.get(f'https://www.instagram.com/api/v1/users/web_profile_info/?username={user}', headers=headers, proxies={'http': proxy})
            try:
                Id = rr.json()['data']['user']['id']
            except:
                Id = ""
            try:
                name = rr.json()['data']['user']['full_name']
            except:
                name = ""
            try:
                bio = rr.json()['data']['user']['biography']
            except:
                bio = ""
            try:
                po = rr.json()['data']['user']['edge_owner_to_timeline_media']['count']
            except:
                po = ""
            try:
                flos = rr.json()['data']['user']['edge_followed_by']['count']
            except:
                flos = ""
            try:
                flog = rr.json()['data']['user']['edge_follow']['count']
            except:
                flog = ""
            try:
                pr = rr.json()['data']['user']['is_private']
            except:
                pr = ""
            try:
                img = rr.json()['data']['user']['profile_pic_url']
            except:
                img = ""

            return {
                'Username': user,
                'Name': name,
                'ID': Id,
                'Followers': flos,
                'Following': flog,
                'Bio': bio,
                'Posts': po,
                'Image': img,
                'Is Private': pr,
                'status': 'ok',
                'By': '@maho_s9'
            }

        except Exception as e:
            return {'state': str(e), 'By': '@maho_s9'}
            
 

class InfoTik:
    @staticmethod
    def TikTok_Info(username):
        try:
            patre = {
                "Host": "www.tiktok.com",
                "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
                "sec-ch-ua-mobile": "?1",
                "sec-ch-ua-platform": "\"Android\"",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; Plume L2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Mobile Safari/537.36",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "sec-fetch-site": "none",
                "sec-fetch-mode": "navigate",
                "sec-fetch-user": "?1",
                "sec-fetch-dest": "document",
                "accept-language": "en-US,en;q=0.9,ar-DZ;q=0.8,ar;q=0.7,fr;q=0.6,hu;q=0.5,zh-CN;q=0.4,zh;q=0.3"
            }

            tikinfo = requests.get(f'https://www.tiktok.com/@{username}', headers=patre).text

            try:
                getting = str(tikinfo.split('webapp.user-detail"')[1]).split('"RecommendUserList"')[0]
                try:
                    id = str(getting.split('id":"')[1]).split('",')[0]
                except:
                    id = ""
                try:
                    name = str(getting.split('nickname":"')[1]).split('",')[0]
                except:
                    name = ""
                try:
                    bio = str(getting.split('signature":"')[1]).split('",')[0]
                except:
                    bio = ""
                try:
                    country = str(getting.split('region":"')[1]).split('",')[0]
                except:
                    country = ""
                try:
                    private = str(getting.split('privateAccount":')[1]).split(',"')[0]
                except:
                    private = ""
                try:
                    followers = str(getting.split('followerCount":')[1]).split(',"')[0]
                except:
                    followers = ""
                try:
                    following = str(getting.split('followingCount":')[1]).split(',"')[0]
                except:
                    following = ""
                try:
                    like = str(getting.split('heart":')[1]).split(',"')[0]
                except:
                    like = ""
                try:
                    video = str(getting.split('videoCount":')[1]).split(',"')[0]
                except:
                    video = ""
                try:
                    secid = str(getting.split('secUid":"')[1]).split('"')[0]
                except:
                    secid = ""
                try:
                    countryn = pycountry.countries.get(alpha_2=country).name
                except:
                    countryn = ""
                try:
                    countryf = pycountry.countries.get(alpha_2=country).flag
                except:
                    countryf = ""

                binary = "{0:b}".format(int(id))
                i = 0
                bits = ""
                while i < 31:
                    bits += binary[i]
                    i += 1
                timestamp = int(bits, 2)
                try:
                    cdt = datetime.fromtimestamp(timestamp)
                except:
                    cdt = ""

                return {                
                    "username": username,
                    "secuid": secid,
                    "name": name,
                    "followers": followers,
                    "following": following,
                    "like": like,
                    "video": video,
                    "private": private,
                    "country": countryn,
                    "flag": countryf,
                    "Date": cdt,
                    "id": id,
                    "bio": bio,
                    "status": "ok",
                    "by": "AHMED"
                }
            except:
                return {
                    "error": "Invalid username",
                    "status": "bad",
                    "by": "AHMED"
                }
        except Exception as e:
            return {            
                "status": "bad",
                "by": "AHMED"
            }           
            
class RestInsta:
    @staticmethod
    def Rest(email):                   
        try:
            csr = md5(str(time.time()).encode()).hexdigest()           
            req = requests.post("https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/", 
                                headers={"User-Agent": generate_user_agent(), 
                                         'x-csrftoken': csr},
                                data={'email_or_username': email},
                                cookies={"csrftoken": csr})
            rest_email = req.json()["contact_point"]
            return {            
                "status": "ok",
                "by": "AHMED",
                "email": rest_email
            }           
        except Exception as e:            
            return {            
                "status": "bad",
                "by": "AHMED",
                "Error": str(e)
            }
            
            
class Spam:
    @staticmethod
    def EmailSpam(email):
        headers = {
            'authority': 'api.kidzapp.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
            'content-type': 'application/json',
            'origin': 'https://kidzapp.com',
            'referer': 'https://kidzapp.com/',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': str(generate_user_agent()),
        }

        json_data = {
            'email': email,
            'sdk': 'web',
            'platform': 'desktop',
        }

        response = requests.post('https://api.kidzapp.com/api/3.0/customlogin/', headers=headers, json=json_data).text
        if 'EMAIL SENT' in response:
            return {'status': 'DONE SEND', 'AHMED': '@maho_s9'}
        else:
            return {'status': 'Sorry Error Send', 'AHMED': '@maho_s9'}
 



class Phrases:
    @staticmethod
    def Wallet(num_words):
        if num_words not in [12, 18, 24]:
            raise ValueError("Number of words must be 12, 18, or 24.")

        mnemo = Mnemonic("english")
        if num_words == 12:
            seed_phrase = mnemo.generate(strength=128)
            return seed_phrase
        elif num_words == 18:
            seed_phrase = mnemo.generate(strength=192)
            
            return seed_phrase
        elif num_words == 24:
            seed_phrase = mnemo.generate(strength=256)
            return seed_phrase



           
            
class UserAgentGenerator:
    dalvik_user_agents = [
        "Dalvik/{}.{} (Linux; U; Android {}; {} Build/{}{})",
        "Dalvik/{}.{} (Linux; Android {}; {} Build/{}{})",
    ]
    devices = [
        "SM-G920F", "Nexus 5", "Nexus 6P", "Pixel 2", "Pixel 4", "Galaxy S10", "Galaxy S20",
        "SM-G975F", "SM-G950F", "SM-G960F", "SM-G970F", "SM-G973F", "SM-G980F",
        "SM-N960F", "SM-N950F", "SM-N970F", "SM-N975F", "SM-N980F", "SM-N985F",
        "P30 Pro", "P20 Pro", "Mate 20 Pro", "Mate 30 Pro", "Mate 40 Pro",
        "Mi 9", "Mi 10", "Mi 11", "Redmi Note 8", "Redmi Note 9", "Redmi Note 10",
        "OnePlus 7", "OnePlus 7T", "OnePlus 8", "OnePlus 8T", "OnePlus 9", "OnePlus 9 Pro",
        "Xperia Z5", "Xperia XZ1", "Xperia XZ2", "Xperia XZ3", "Xperia 1", "Xperia 5",
        "HTC U11", "HTC U12+", "HTC 10", "HTC One M9", "HTC One M8",
        "LG G6", "LG G7 ThinQ", "LG V30", "LG V40 ThinQ", "LG V50 ThinQ",
        "Google Pixel", "Google Pixel XL", "Google Pixel 2 XL", "Google Pixel 3", "Google Pixel 3 XL",
        "Galaxy A50", "Galaxy A51", "Galaxy A70", "Galaxy A71", "Galaxy A80", "Galaxy A90",
    ]
    versions = [
        "7.0", "7.1.1", "8.0.0", "8.1.0", "9", "10", "11"
    ]
    brands = [
        "Google", "Samsung", "Huawei", "Sony", "HTC", "OnePlus", "Xiaomi", "LG"
    ]

    def __str__(self):
        template = random.choice(self.dalvik_user_agents)
        android_version = random.choice(self.versions)
        device = random.choice(self.devices)
        brand = random.choice(self.brands)
        generate_version = random.randint(1, 99)
        return template.format(generate_version, generate_version, android_version, brand, device, generate_version)

