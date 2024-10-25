# coding=utf-8
from flask import Flask, request, jsonify, make_response, render_template
import lock_V3
import unlock_V3
import os
import time
import datetime
import requests

base_path = "/data/" if os.path.exists("/.dockerenv") else os.path.dirname(__file__)
app = Flask(__name__)
BlackSet = {}


@app.route("/")
def index():
    # 根据 URL 参数进行加密或解密
    text = request.args.get("text")
    password = request.args.get("password")
    
    if text:
        # 对 text 进行加密
        encrypted_text = lock_V3.lock(text)
        return jsonify({"encrypted": encrypted_text})
    
    if password:
        # 对 password 进行解密
        decrypted_text = unlock_V3.unlock(password)
        if decrypted_text:
            return jsonify({"decrypted": decrypted_text})
        else:
            return make_response(jsonify({"error": "解密失败！密文不合法"}), 400)
    
    # 如果没有参数，则返回默认的主页
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr

    if client_ip != "127.0.0.1":
        log_visitor(client_ip)

    return render_template("index.html")


def log_visitor(ip):
    now = datetime.datetime.now()
    time1 = now.strftime("%Y-%m-%d %H:%M:%S")
    location_info = get_location(ip)
    country = location_info.get("country", "Unknown")
    province = location_info.get("regionName", "Unknown")
    city = location_info.get("city", "Unknown")
    with open(os.path.join(base_path, "visitors.log"), "a") as f:
        f.write(f"IP: {ip}\tAddress: {country}-{province}-{city}\tTime: {time1}\n")


def get_location(ip_address):
    url = f"http://ip-api.com/json/{ip_address}?lang=zh-CN"
    try:
        response = requests.get(url, timeout=3)
        data = response.json()
    except requests.RequestException:
        data = {}
    return data


@app.route("/lock", methods=["POST"])
def lock():
    data = request.get_json()
    message = data.get("message")
    if message and message.strip():
        return jsonify({"response": lock_V3.lock(message)})
    else:
        return make_response(jsonify({"response": ""}), 400)


@app.route("/unlock", methods=["POST"])
def unlock():
    data = request.get_json()
    message = data.get("message")
    if message and message.strip():
        response = unlock_V3.unlock(message)
        if response:
            return jsonify({"response": response})
        else:
            return make_response(jsonify({"response": "解密失败！密文不合法"}), 400)
    else:
        return make_response(jsonify({"response": ""}), 400)


def is_allowed_to_send_message(ip_address):
    current_time = time.time()
    last_message_time = BlackSet.get(ip_address, 0)
    if current_time - last_message_time < 60:
        return False
    return True


@app.route("/message", methods=["POST"])
def message():
    data = request.get_json()
    message_content = data.get("message")
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr

    if client_ip != "127.0.0.1":
        if not is_allowed_to_send_message(client_ip):
            return make_response(
                jsonify({"response": "留言失败，一分钟内只能发送一条留言"}), 400
            )

        log_visitor(client_ip)
        current_time = time.time()
        BlackSet[client_ip] = current_time

        now = datetime.datetime.now()
        time1 = now.strftime("%Y-%m-%d %H:%M:%S")

        location_info = get_location(client_ip)
        country = location_info.get("country", "Unknown")
        province = location_info.get("regionName", "Unknown")
        city = location_info.get("city", "Unknown")

        with open(os.path.join(base_path, "message.txt"), "a") as f:
            f.write(
                f"IP:{client_ip}\tAddress:{country}-{province}-{city}\tTime:{time1}:\n"
            )
            f.write(f"{message_content}\n\n")

    return jsonify({"response": "谢谢留言，我已收到❤️"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8101)
