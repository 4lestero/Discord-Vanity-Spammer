import time
import requests
import random

WEBHOOK_URL = "" 

def send_to_webhook(content):
    data = {
        "content": content
    }
    requests.post(WEBHOOK_URL, json=data)

def load_tokens_from_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

TOKENS = load_tokens_from_file("tokens.txt")
VANITY_URL = "1876"
GUILD_ID = "1201902829514801172"
API_URL = f"https://canary.discord.com/api/v10/guilds/{GUILD_ID}/vanity-url"
DELAY = 0.155  # Saniye cinsinden

HEADERS = {
    "Authorization": "{}", 
    "Content-Type": "application/json"
}

token_counts = {token: 0 for token in TOKENS}
total_requests = 0

def change_vanity_url(token):
    global total_requests
    headers = HEADERS.copy()
    headers["Authorization"] = headers["Authorization"].format(token)

    payload = {
        "code": VANITY_URL
    }

    response = requests.patch(API_URL, headers=headers, json=payload)

    token_counts[token] += 1
    total_requests += 1

    if response.status_code != 200:
        print(f"Token: {token}, Status Code: {response.status_code}, Response: {response.text}")
        return False

    return True

def main():
    last_webhook_update = time.time()

    while True:
        token = random.choice(TOKENS)

        if change_vanity_url(token):
            print("Vanity URL başarıyla alındı!")
            break

        current_time = time.time()
        if current_time - last_webhook_update > 600:  # 10 dakika kontrolü
            time_left = 3600 - (current_time - last_webhook_update) 
            nearly_limited_tokens = [k for k, v in token_counts.items() if v >= 45]

            message = f"1 saat dolmasına {time_left//60} dakika kaldı.\n"
            message += f"Toplamda {total_requests} istek atıldı.\n"
            if nearly_limited_tokens:
                message += f"Bu tokenlar yakında sınırlandırılabilir: {', '.join(nearly_limited_tokens)}"

            send_to_webhook(message)
            last_webhook_update = current_time

        time.sleep(DELAY)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ana hatayı yakalama: {e}")

    input("Betiği kapatmadan önce bir tuşa basın...")
