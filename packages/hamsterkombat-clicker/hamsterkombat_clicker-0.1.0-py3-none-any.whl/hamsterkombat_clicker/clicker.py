import requests
import time
import random

class HamsterKombatClicker:
    def __init__(self, url, headers_template, bearer_tokens, count_interval=(1, 5), sleep_interval=(10, 300)):
        self.url = url
        self.headers_template = headers_template
        self.bearer_tokens = bearer_tokens
        self.count_interval = count_interval
        self.sleep_interval = sleep_interval

    def add_token(self, token):
        """Add a new bearer token to the list."""
        self.bearer_tokens.append(token)

    def remove_token(self, token):
        """Remove a bearer token from the list."""
        if token in self.bearer_tokens:
            self.bearer_tokens.remove(token)

    def send_request(self, token, body):
        """Send a POST request with the provided bearer token and body."""
        headers = self.headers_template.copy()
        headers["Authorization"] = f"Bearer {token}"
        response = requests.post(self.url, json=body, headers=headers)
        return response

    def execute(self):
        """Continuously send requests at intervals."""
        while True:
            timestamp = int(time.time())
            count = random.randint(*self.count_interval)
            print(f"\nTapping count: {count}\n")

            body = {
                "count": count,
                "availableTaps": 5000,
                "timestamp": timestamp
            }

            for token in list(self.bearer_tokens):
                try:
                    response = self.send_request(token, body)
                    if response.status_code == 200:
                        print("Response:", response.json())
                        print("\nRequest successful!\n")
                    elif response.status_code in {401, 403}:
                        print("Response:", response.text)
                        print(f"\nInvalid token detected. Removing token: {token}\n")
                        self.remove_token(token)
                        print(f"Remaining tokens: {self.bearer_tokens}")
                    else:
                        print("Response:", response.text)
                        print("\nRequest failed with status code:", response.status_code)
                        print("Waiting for 5 minutes before retrying...\n")
                        time.sleep(300)
                except requests.exceptions.RequestException as e:
                    print(f"An error occurred: {e}")
                    print("Waiting for 10 minutes before retrying...\n")
                    time.sleep(600)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    print("Waiting for 10 minutes before retrying...\n")
                    time.sleep(600)

            sleep_duration = random.randint(*self.sleep_interval)
            print(f"\nSleeping for {sleep_duration} seconds\n")
            time.sleep(sleep_duration)
