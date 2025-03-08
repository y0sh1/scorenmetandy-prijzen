import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import re

def extract_fuel_prices(url):
    now = datetime.now()

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Failed to load the webpage.")

    os.makedirs('examples/', exist_ok=True)
    with open(f'examples/fuel_prices_{now.strftime("%Y%m%d_%H%M%S")}.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    soup = BeautifulSoup(response.content, "html.parser")

    text = soup.get_text()

    pattern = r"(diesel|Euro 95|Superplus) voor €(\d+,\d+)"
    matches = re.findall(pattern, text)
    fuel_prices = {fuel: float(price.replace(',', '.')) for fuel, price in matches}
    json_output = json.dumps(fuel_prices, indent=4)

    message = ":rocket: *Nieuwe Scoren met Andy prijzen!* :sunglasses:\n"
    emoji_dict = {"diesel": ":oil_drum:", "Euro 95": ":fuelpump:", "Superplus": ":racing_car:"}
    for fuel, price in fuel_prices.items():
        message += f"{emoji_dict.get(fuel, ':fuelpump:')} *{fuel}*: €{price:.2f}\n"

    slack_data = {'text': message}
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if not webhook_url:
        raise Exception("Environment variable SLACK_WEBHOOK_URL not set")
    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise Exception("Failed to send message to Slack")

    return json_output

url = "http://scorenmetandy.nl"
print(extract_fuel_prices(url))
