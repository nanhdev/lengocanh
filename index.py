from flask import Flask, request, jsonify, redirect
import nanhget
import asyncio

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

    # Xử lý API nếu có đủ cookie và imei
    data = asyncio.run(nanhget.main(imei, cookie_dict))


    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
