from flask import Flask, jsonify, request
import nanhget
import asyncio
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)

@app.route('/zlapi/login', methods=['GET'])
def login():
    cookies = request.headers.get('Cookie', '')
    imei = request.args.get('imei', '')
    if not imei or not cookies:
        return jsonify({"error": "Missing required parameters"}), 400

    cookie_dict = {k: v for k, v in (cookie.split('=') for cookie in cookies.split('; '))}
    data = asyncio.run(nanhget.main(imei, cookie_dict))
    return jsonify(data)

# ASGI compatibility for Vercel
app_asgi = WsgiToAsgi(app)
