from flask import Flask, request, jsonify, redirect
import nanhget
import asyncio
from asgiref.wsgi import WsgiToAsgi  # Thêm để hỗ trợ ASGI

app = Flask(__name__)

@app.route('/zlapi/login', methods=['GET'])
def get_cookie():
    all_cookies = request.headers.get('Cookie')
    cookie_dict = {}

    if all_cookies:
        cookies = all_cookies.split("; ")
        for cookie in cookies:
            key, value = cookie.split("=", 1)
            cookie_dict[key] = value

    imei = request.args.get('imei')

    if imei is None or not cookie_dict:
       data = {
          'error_code': 403,
         ' error_message': "Quốc Khánh Đz Vờ Lờ"
       }
       return data

    # Xử lý API nếu có đủ cookie và imei
    data = asyncio.run(nanhget.main(imei, cookie_dict))

    return jsonify(data)

# Tương thích với ASGI
app_asgi = WsgiToAsgi(app)
