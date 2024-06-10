import requests
import hashlib

def check_account(email, password):
    session = requests.Session()
    data = {
        "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
        "email": email,
        "password": password,
        "locale": "en_US",
        "format": "JSON"
    }

    sig = ''.join([f'{key}={value}' for key, value in data.items()])
    data['sig'] = hashlib.md5(sig.encode('utf-8')).hexdigest()

    headers = {
        "User-Agent": "Opera/9.80 (Series 60; Opera Mini/7.0.32400/28.3445; U; en) Presto/2.8.119 Version/11.10"
    }

    response = session.post("https://api.facebook.com/method/auth.login", data=data, headers=headers)
    result = response.json()
    try:
        result = response.json()
        return str(result['access_token'])
    except Exception as e:
        print(e)
        return "Authentication failed"