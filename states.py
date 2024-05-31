import comms
import mgmt
import signin_timer
import time

timer = None


class state:
    # for signed out
    def pin_sign_in(self, pin: str): return
    def card_sign_in(self, id: str|None, value: str|None): return
    def card_sign_up(self): return  ##TODO
    # for signed in
    def get_motors(self, ): return
    def motor_action(self, motor_id : str, action: str): return
    def on_status_received(self, status): return
    def print(self): return


class signed_out_state(state):
    def __init__(self) -> None:
        global timer
        self.print()
        if timer is not None:
            timer.terminate()
            timer = None
    def pin_sign_in(self, pin: str):
        global global_state
        result =  comms.sign_in_pin(pin)
        if result is not False:
            global_state = signed_in_state(result[0], result[1])
        else:
            mgmt.io.emit("message", {"login_error":"Pin is not recognised, try again"})
        return result
    
    def card_sign_in(self, id: str|None, value: str|None):
        if(id is None or value is None):
            return False
        global global_state
        result = comms.sign_in_card(id, value)
        if result is not False:
            global_state = signed_in_state(result[0], result[1])
        else:
            mgmt.io.emit("message", {"login_error":"Card is not recognised, try again"})
        return result
    
    def print(self): 
        mgmt.io.emit("message", {"signout":{}})
    
class signed_in_state(state):
    read_card_id = read_card_value = None
    def __init__(self, token: str, expires: str):
        global timer
        self.token = token 
        self.expires = expires
        self.whoami = comms.whoami()
        self.print()
        timer = signin_timer.timer(expires - time.time())

    def get_motors(self):
        motors = comms.get_motors()
        mgmt.io.emit("message", {"motors":motors})
        return motors

    def motor_action(self, motor_id: str, action: str):
        comms.motor_action(motor_id, action)

    def on_status_received(self, status):
        mgmt.io.emit("message", {"status":status})

    def print(self):
        mgmt.io.emit("message", {"signin":{"token":self.token, "expires": self.expires}, "whoami":self.whoami})

    def card_sign_in(self, id: str|None, value: str|None):
        self.read_card_id = id
        self.read_card_value = value



global_state = signed_out_state()