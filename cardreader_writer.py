import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import threading
from time import sleep
import states

rfid = SimpleMFRC522()

read_card = card_to_write = None

def keep_scanning():
    global read_card, card_to_write
    while True:
        sleep(0.5)
        #go for next iteration
        id, text = rfid.read_no_block()
        
        if(id is not None and text is not None):
            print(id, text)
            #check the received card data """
        states.global_state.card_sign_in(id, text)
        if card_to_write is not None:
            rfid.write(card_to_write)
            card_to_write = None


scanner_thread = threading.Thread(target=keep_scanning)
scanner_thread.start()
