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
        return redirect("https://guns.lol/nanh")  

    # Chạy các tác vụ bất đồng bộ
    loop = asyncio.new_event_loop()  # Tạo vòng lặp sự kiện mới
    asyncio.set_event_loop(loop)  # Đặt vòng lặp sự kiện mới cho thread hiện tại
    data = loop.run_until_complete(nanhget.main(imei, cookie_dict))  # Chạy async function

    return jsonify(data)
# Tương thích với ASGI
app_asgi = WsgiToAsgi(app)
