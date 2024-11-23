from quart import Quart, request, jsonify, redirect
import requests
from datetime import datetime

app = Quart(__name__)

class ZaloAPI:
    def __init__(self, api_domain, api_type, api_version):
        self.authDomain = api_domain
        self.apiType = api_type
        self.apiVersion = api_version

    async def get_login_info(self, imei, cookie, language="vi", local_ip="", screen_size=None, info="", source_install=None, additional_params=None, is_new=0):
        url = f"{self.authDomain}/api/login/getLoginInfo"
        params = {
            'imei': imei,
            'computer_name': "web",
            'language': language,
            'ts': int(datetime.utcnow().timestamp() * 1000)
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

        response = requests.get(url, headers=HEADERS, params=params, cookies=cookie).json()
        return response

@app.route('/zlapi/login', methods=['GET'])
async def get_cookie():
    all_cookies = request.headers.get('Cookie')
    cookie_dict = {}

    if all_cookies:
        cookies = all_cookies.split("; ")
        for cookie in cookies:
            key, value = cookie.split("=", 1)
            cookie_dict[key] = value

    imei = request.args.get('imei')

    if imei is None or not cookie_dict:
        return redirect("https://guns.lol/nanh")  

    # Chạy tác vụ bất đồng bộ trực tiếp trong Quart
    api = ZaloAPI("https://wpa.chat.zalo.me", "30", "637")
    data = await api.get_login_info(imei, cookie_dict)  

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
