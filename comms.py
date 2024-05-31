import sys

if len(sys.argv) < 3:
    raise "Not enough arguments to start, required: [HOST] [APP_ID] [APP_TOKEN]"
    exit(0)

prefix = sys.argv[1]
app_id = sys.argv[2]
app_token = sys.argv[3]

token = expires = None

import requests
import json
import mgmt

def sign_in_pin(pin : str):
    global token, expires
    try:
        req_res = requests.post(prefix + "auth/app" + str(app_id) + ":" + app_token + "/pin/" + pin, timeout=3)
    except Exception as e:
        mgmt.io.emit("server_is_not_discoverable", {"server_address":prefix})
        return False
    if(req_res.status_code != 200):
        return False
    content = req_res.content
    result = json.loads(content)
    token = result["response"]["token"]
    expires = result["response"]["expires"]
    return (token, expires)
    
def sign_in_card(card_id: str, card_token:str):
    global token, expires
    card_token = str(card_token).strip()
    try:
        req_res = requests.post(prefix + "auth/app" + str(app_id) + ":" + str(app_token) + "/card/" + str(card_id) + "/" + str(card_token), timeout=3)
    except Exception as e:
        mgmt.io.emit("server_is_not_discoverable", {"server_address":prefix})
        return False
    if(req_res.status_code != 200):
        return False
    content = req_res.content
    result = json.loads(content)
    token = result["response"]["token"]
    expires = result["response"]["expires"]
    return (token, expires)

def register_card(card_id: str, card_token: str):
    global token, expires
    try:
        req_res = requests.post(prefix + "auth/app" + str(app_id) + ":" + app_token + "/card/" + card_id + "/" + card_token, timeout=3)
    except Exception as e:
        mgmt.io.emit("server_is_not_discoverable", {"server_address":prefix})
        return False
    if(req_res.status_code != 200):
        return False

def get_motors():
    global token, expires
    try:
        req_res = requests.get(prefix + "motors/", {'access_token':token}, timeout=3)
    except Exception as e:
        mgmt.io.emit("server_is_not_discoverable", {"server_address":prefix})
        return False
    if(req_res.status_code != 200):
        return False
    content = req_res.content
    result = json.loads(content)
    return (result["response"])

def open_motor(motor_id : str):
    global token, expires
    try:
        req_res = requests.post(prefix + "motors/" + motor_id + "/open", {'access_token':token}, timeout=3)
    except Exception as e:
        mgmt.io.emit("server_is_not_discoverable", {"server_address":prefix})
        return False
    return req_res.status_code == 204

def close_motor(motor_id:str):
    global token, expires
    try:
        req_res = requests.post(prefix + "motors/" + motor_id + "/close", {'access_token':token}, timeout=3)
    except Exception as e:
        mgmt.io.emit("server_is_not_discoverable", {"server_address":prefix})
        return False
    return req_res.status_code == 204
    
def motor_action(motor_id: str, action: str):
    global token, expires
    try:
        req_res = requests.post(prefix + "motors/" + motor_id + "/" + action, {'access_token':token}, timeout=3)
    except Exception as e:
        mgmt.io.emit("server_is_not_discoverable", {"server_address":prefix})
        return False
    return req_res.status_code == 204

def whoami():
    global token, expires 
    try:
        req_res = requests.get(prefix + "users/whoami", {'access_token':token}, timeout=3)
    except Exception as e:
        mgmt.io.emit("server_is_not_discoverable", {"server_address":prefix})
        return False
    if req_res.status_code == 200:
        try:
            return req_res.json()
        except Exception:
            pass

    return False

def register_card(card_id: str):
    global token, expires
    try:
        req_res = requests.post(prefix + "users/register_card/" + str(card_id), {'access_token':token}, timeout=3)
    except Exception as e:
        mgmt.io.emit("server_is_not_discoverable", {"server_address":prefix})
        return False
    if req_res.status_code == 200:
        try: return req_res.json()["response"]
        except Exception: pass
    return False
