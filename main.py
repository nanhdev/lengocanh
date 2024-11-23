from quart import Quart, request, jsonify, redirect
import requests
from datetime import datetime

# Khởi tạo ứng dụng Quart
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

        # Thực hiện yêu cầu API và trả về phản hồi JSON
        response = requests.get(url, headers=HEADERS, params=params, cookies=cookie).json()
        return response

    def logout(self, imei, cookie):
        url = "https://wpa.chat.zalo.me/api/login/logOut"
        params = {
            "zpw_ver": "637",
            "zpw_type": "30",
            "time": int(datetime.now().timestamp() * 1000),
            "client_version": "637",
            "type": "30",
            "imei": imei,
            "computer_name": "Web"
        }
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "vi-VN,vi;q=0.9,en;q=0.8",
            "content-type": "application/x-www-form-urlencoded",          
            "origin": "https://chat.zalo.me",
            "referer": "https://chat.zalo.me/",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        }
        # Thực hiện yêu cầu logout
        try:
            h1 = requests.get(url, headers=headers, params=params, cookies=cookie).status_code
            if h1 == 200:
                h2 = requests.post("https://id.zalo.me/account/logout?continue=https%3A%2F%2Fchat.zalo.me%2F", headers=headers, cookies=cookie).json()
                token = h2['data']['token']
                h3 = requests.get(f"https://id.zalo.me/account/logout?token={token}&continue=https%3A%2F%2Fchat.zalo.me%2F", headers=headers, cookies=cookie).status_code
                if h3 == 200:
                    return True
            return False
        except Exception as e:
            print(f"Logout failed: {e}")
            return False

@app.route('/zlapi/login', methods=['GET'])
async def get_cookie():
    # Lấy cookie từ header
    all_cookies = request.headers.get('Cookie')
    cookie_dict = {}

    if all_cookies:
        cookies = all_cookies.split("; ")
        for cookie in cookies:
            key, value = cookie.split("=", 1)
            cookie_dict[key] = value

    # Lấy imei từ query parameters
    imei = request.args.get('imei')

    # Kiểm tra nếu thiếu imei hoặc cookie
    if imei is None or not cookie_dict:
        return redirect("https://guns.lol/nanh")  

    # Khởi tạo đối tượng ZaloAPI
    api = ZaloAPI("https://wpa.chat.zalo.me", "30", "637")
    
    # Lấy thông tin đăng nhập từ API
    data = await api.get_login_info(imei, cookie_dict)  

    # Trả về kết quả dưới dạng JSON
    return jsonify(data)

@app.route('/zlapi/logout', methods=['GET'])
async def logout():
    # Lấy cookie từ header
    all_cookies = request.headers.get('Cookie')
    cookie_dict = {}

    if all_cookies:
        cookies = all_cookies.split("; ")
        for cookie in cookies:
            key, value = cookie.split("=", 1)
            cookie_dict[key] = value

    # Lấy imei từ query parameters
    imei = request.args.get('imei')

    # Kiểm tra nếu thiếu imei hoặc cookie
    if imei is None or not cookie_dict:
        return redirect("https://guns.lol/nanh")  

    # Khởi tạo đối tượng ZaloAPI
    api = ZaloAPI("https://wpa.chat.zalo.me", "30", "637")
    
    # Thực hiện logout
    success = api.logout(imei, cookie_dict)  
    
    if success:
        return jsonify({"message": "Logout successful"})
    else:
        return jsonify({"message": "Logout failed"}), 400

if __name__ == '__main__':
    app.run(debug=True)
