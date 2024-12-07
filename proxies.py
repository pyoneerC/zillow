import requests

def load_proxies(file_path):
    try:
        with open(file_path, "r") as file:
            proxies = file.read().splitlines()
        return proxies
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []

def test_proxy(proxy):
    test_url = "https://httpbin.org/ip"
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    try:
        response = requests.get(test_url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(f"Proxy {proxy} is working. Response: {response.json()}")
            return True
    except requests.exceptions.RequestException as e:
        print(f"Proxy {proxy} failed. Error: {e}")
    return False

def test_proxies(file_path):
    proxies = load_proxies(file_path)
    if not proxies:
        print("No proxies to test.")
        return

    working_proxies = []
    for proxy in proxies:
        if test_proxy(proxy):
            working_proxies.append(proxy)

    with open("working_proxies.txt", "w") as file:
        for proxy in working_proxies:
            file.write(proxy + "\n")

    print(f"Working proxies saved to working_proxies.txt. Total: {len(working_proxies)}")

if __name__ == "__main__":
    test_proxies("proxies.txt") # (https://github.com/TheSpeedX/PROXY-List/blob/master/socks5.txt)
