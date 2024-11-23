from quart import Quart, request, jsonify, redirect
import nanhget
import asyncio

app = Quart(__name__)

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
    data = await nanhget.main(imei, cookie_dict)  

    return jsonify(data)
# Tương thích với ASGI
app_asgi = WsgiToAsgi(app)
