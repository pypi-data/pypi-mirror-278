# Hamster Kombat Clicker

A package to interact with the Hamster Kombat Clicker API.

## Installation

Install the package using pip:

```bash
pip install hamsterkombat_clicker
```

## Usage

### Basic Usage

```python
from hamsterkombat_clicker.clicker import HamsterKombatClicker

url = "https://api.hamsterkombat.io/clicker/tap"
headers_template = {
    "Content-Type": "application/json"
}

bearer_tokens = [
    "your_token_here"
]

# Initialize the clicker with default intervals
clicker = HamsterKombatClicker(url, headers_template, bearer_tokens)
clicker.execute()
```

### Configurable Intervals

You can provide optional parameters for `count_interval` and `sleep_interval` to customize the random tapping count and sleep duration.

```python
clicker = HamsterKombatClicker(
    url, 
    headers_template, 
    bearer_tokens, 
    count_interval=(2, 6),  # Custom interval for tapping count
    sleep_interval=(20, 400)  # Custom interval for sleep duration in seconds
)
clicker.execute()
```

## Obtaining a Bearer Token

To get a bearer token, follow these steps:

1. **Launch Hamster Kombat in the Browser**: You need to start Hamster Kombat in your web browser. You can find detailed instructions on how to do this [here](https://github.com/EvgeniyVorobev/hamster-kombat-bot/blob/main/README.md).

2. **Open Developer Tools**: In your web browser (Chrome, Firefox, etc.), open the Developer Tools. This is usually done by pressing `F12` or `Ctrl+Shift+I`.

3. **Navigate to the Network Tab**: Go to the `Network` tab in the Developer Tools.

4. **Find the Request**: Look for a network request named `me-telegram` in the list of network requests.

5. **Copy the Token**: In the `me-telegram` request, locate the `Authorization` header. The value will be in the format `Bearer <token>`. Copy the token part without the `Bearer` prefix.

### Example of Obtaining the Token

1. Open Hamster Kombat in your browser.
2. Open Developer Tools and navigate to the Network tab.
3. Find the `me-telegram` request.
4. Copy the token from the `Authorization` header.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Author

Your Name - [diyarbekdev@gmail.com](mailto:diyarbekdev@gmail.com)

## Disclaimer

### This package is intended for educational purposes only. It demonstrates how to interact with an API and manage HTTP requests programmatically. The usage of this package should comply with all applicable laws and terms of service of the API it interacts with. The author is not responsible for any misuse of this package.
