import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse
load_dotenv()

API_KEY = os.getenv("API_VK_Skey")
BASE_URL = "https://api.vk.com/method/"


def shorten_link(long_link):
    method = "utils.getShortLink"
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }
        params = {
            "v": "5.199",
            "url": long_link,
        }
        url = f"{BASE_URL}{method}"
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if "error" in data:
            return f"VK API ошибка: {data['error']['error_msg']}"
        else:
            return data["response"]["short_url"]
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе: {e}"


def count_clicks(link):
    method = "utils.getLinkStats"
    parsed = urlparse(link)
    link = parsed.path.lstrip("/")
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }
        params = {
            "v": "5.199",
            "key": link,
            "interval": "forever"
        }
        url = f"{BASE_URL}{method}"
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        stats = data.get("response", {}).get("stats", [])
        if stats:
            return stats[0].get("views", 0)
        else:
            return "Нет переходов"
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе: {e}"


def is_shorten_link(url):
    method = "utils.getLinkStats"
    parsed = urlparse(url)
    link = parsed.path.lstrip("/")
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }
        params = {
            "v": "5.199",
            "key": link,
            "interval": "forever"
        }
        url = f"{BASE_URL}{method}"
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        return data.get("response", {}).get("stats") is not None
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе: {e}"


def main():
    link = input("Введите ссылку: ").strip()

    if is_shorten_link(link):
        print("Количество кликов: ", count_clicks(link))
    else:
        print("Сокращенная ссылка: ", shorten_link(link))


if __name__ == "__main__":
    main()
