from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import time
import states
import mgmt
import comms
import threading
import cardreader_writer


@mgmt.app.get("/")
def root_page():
    return render_template('login_screen.html')

@mgmt.io.on("get_state")
def get_state():
    return states.global_state.print()

@mgmt.io.on("connect")
def on_connect():
    return get_state()

@mgmt.io.on("login_attempt_pin")
def on_login_attempt_pin(data):
    return states.global_state.pin_sign_in(data["pin"])

@mgmt.io.on("get_devices")
def get_devices():
    print("get_devices called")
    return states.global_state.get_motors()

@mgmt.io.on("motor_open")
def motor_open(data):
    return states.global_state.motor_action(data, 'open')

@mgmt.io.on("motor_close")
def motor_close(data):
    return states.global_state.motor_action(data, 'close')

@mgmt.io.on("signout")
def signout(data = None):
    if states.timer is not None:
        states.timer.terminate()
        states.timer = None
    return

@mgmt.io.on('register_card')
def register_card():
    if (states.global_state.read_card_id is None):
        mgmt.io.emit("register_card_result", {"problem":"No card found"})
        return
    res = comms.register_card(states.global_state.read_card_id)
    if res is False:
        mgmt.io.emit("register_card_result", {"problem":"Card registration failed"})
        return
    else:
        import cardreader_writer
        cardreader_writer.card_to_write = res
        mgmt.io.emit("register_card_result", True)

def motor_reporter():
    while True:
        states.global_state.get_motors()
        time.sleep(1)

reporter_thread = threading.Thread(target=motor_reporter)
reporter_thread.start()

mgmt.app.run(port=5000, threaded=True)