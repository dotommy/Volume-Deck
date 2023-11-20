import random
import json
import os

json_file = 'otp.json'

def otp_generator():

    otp = random.randint(1000, 9999)

    return otp

def save_otp_in_json(otp):
    with open(json_file, 'w') as file:
        json.dump({'otp': otp}, file)

def read_otp_da_json():
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            return data.get('otp')
    except FileNotFoundError:
        return None

def remove_json():
    try:
        os.remove(json_file)
    except FileNotFoundError:
        pass