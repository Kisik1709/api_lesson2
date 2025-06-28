import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse


BASE_URL = "https://api.vk.com/method/"


def shorten_link(token, long_link):
    method = "utils.getShortLink"

    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "v": "5.199",
        "url": long_link,
    }
    url = f"{BASE_URL}{method}"
    response = requests.get(url, headers=headers, params=params)
    json_data = response.json()
    if "error" in json_data:
        return f"VK API ошибка: {json_data['error']['error_msg']}"
    else:
        return json_data["response"]["short_url"]


def count_clicks(token, link):
    method = "utils.getLinkStats"
    parsed_url = urlparse(link)
    link = parsed_url.path.lstrip("/")

    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "v": "5.199",
        "key": link,
        "interval": "forever"
    }
    url = f"{BASE_URL}{method}"
    response = requests.get(url, headers=headers, params=params)
    json_data = response.json()
    stats = json_data.get("response", {}).get("stats", [])
    if stats:
        return stats[0].get("views", 0)
    else:
        return "Нет переходов"


def is_shorten_link(token, user_link):
    method = "utils.getLinkStats"
    parsed_url = urlparse(user_link)
    short_link = parsed_url.path.lstrip("/")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "v": "5.199",
        "key": short_link,
        "interval": "forever"
    }
    url = f"{BASE_URL}{method}"
    response = requests.get(url, headers=headers, params=params)
    json_data = response.json()
    return "response" in json_data and "stats" in json_data["response"]


def main():
    load_dotenv()
    token = os.getenv("API_VK_SKEY")
    if not token:
        print("Ошибка: переменная окружения токена не найдена")
        return

    user_link = input("Введите ссылку: ").strip()

    try:
        if is_shorten_link(token, user_link):
            print("Количество кликов: ", count_clicks(token, user_link))
        else:
            print("Сокращенная ссылка: ", shorten_link(token, user_link))
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")


if __name__ == "__main__":
    main()
