import json
import requests
from datetime import datetime

class ZaloAPI:
    def __init__(self, api_domain, api_type, api_version ):
        self.authDomain = api_domain
        self.apiType = api_type
        self.apiVersion = api_version
    async def get_login_info(self, imei,cookie, language="vi", local_ip="", screen_size=None, info="", source_install=None, additional_params=None, is_new=0 ,):
        url = f"{self.authDomain}/api/login/getLoginInfo"
        params = {
            'imei': imei,
            'computer_name': "web",
            'language': language,
            'ts':int(datetime.utcnow().timestamp() * 1000)
        }
        HEADERS = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
	"Accept": "application/json, text/plain, */*",
	"sec-ch-ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
	"sec-ch-ua-mobile": "?0",
	"sec-ch-ua-platform": "\"Linux\"",
	"origin": "https://chat.zalo.me",
	"sec-fetch-site": "same-site",
	"sec-fetch-mode": "cors",
	"sec-fetch-dest": "empty",
	"referer": "https://chat.zalo.me/",
	"accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
}


        response = requests.get(url, headers=HEADERS,params=params,cookies=cookie).json()
  

        return response



async def main(imei, cookie):
    api = ZaloAPI("https://wpa.chat.zalo.me", "30", "637")
    
    response = await api.get_login_info(imei, cookie)
    
    if response['error_code'] == 0:
        zpw_enk = response['data']['zpw_enk']
        phone = response['data']['phone_number']
        semid_2 = response['data']['send2me_id']
        

        data = {
            'error_code': 0,
            'data': {
                'secret_key': zpw_enk,
                'send2me_id': semid_2,
                'phone_number': phone,
                "zpw_ws": response['data']['zpw_ws']
            }
        }
        

        with open(f'data/{phone}.txt', 'w') as file:
            z = f"imei={imei} \ncookie={cookie}"
            file.write(z + '\n')
        
        return data
    else:
        data = {
            'error_code': response['error_code'],
            'error_message': f"{response['error_message']}"
        }
        return data


