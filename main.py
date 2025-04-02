import requests
from bs4 import BeautifulSoup
import json
import os
import re
import time

def extract_fuel_prices(url):
    # Fetch current webpage
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to load the webpage.")

    # Parse HTML and extract prices
    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.get_text()
    pattern = r"(diesel|Euro 95|Superplus) voor €(\d+,\d+)"
    matches = re.findall(pattern, text)
    current_prices = {fuel: float(price.replace(',', '.')) for fuel, price in matches}

    # Load previous prices
    state_file_path = 'examples/fuel_prices_state.json'
    os.makedirs(os.path.dirname(state_file_path), exist_ok=True)
    
    try:
        with open(state_file_path, 'r', encoding='utf-8') as file:
            previous_prices = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        previous_prices = {}

    # Check for price changes
    if current_prices == previous_prices:
        print("No price changes detected.")
        return None

    # Send Slack notification
    message = ":rocket: _Nieuwe Scoren met Andy prijzen!_ :sunglasses:\n"
    emoji_dict = {"diesel": ":oil_drum:", "Euro 95": ":fuelpump:", "Superplus": ":racing_car:"}
    for fuel, price in current_prices.items():
        message += f"{emoji_dict.get(fuel, ':fuelpump:')} _{fuel}_: €{price:.2f}\n"

    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if not webhook_url:
        raise Exception("Environment variable SLACK_WEBHOOK_URL not set")
    
    response = requests.post(
        webhook_url,
        data=json.dumps({'text': message}),
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code != 200:
        raise Exception("Failed to send message to Slack")

    return current_prices

url = "http://scorenmetandy.nl"
state_file_path = 'examples/fuel_prices_state.json'

while True:
    try:
        new_prices = extract_fuel_prices(url)
        if new_prices is not None:
            with open(state_file_path, 'w', encoding='utf-8') as file:
                json.dump(new_prices, file, indent=4)
            print("Prices updated:", json.dumps(new_prices, indent=4))
    except Exception as e:
        print("Error:", str(e))
    
    time.sleep(900)