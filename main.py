import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse
import argparse


def shorten_link(headers, url):
    body = {
        "long_url":url
    }
    response = requests.post("https://api-ssl.bitly.com/v4/shorten/",headers=headers,
                             json=body)
    response.raise_for_status()
    return response.json()['id']


def count_clicks(headers, short_link):
    sum_url = f"https://api-ssl.bitly.com/v4/bitlinks/{short_link}/clicks/summary"
    response = requests.get(sum_url,headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(headers, bitlink):
    bitl = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    response = requests.get(bitl,headers=headers)
    return response.ok


def main():
    apikey_bitly = os.environ('APIKEY_BITLY')
    headers = {
    "Authorization": f"Bearer {apikey_bitly}",
    }
    parser = argparse.ArgumentParser(
        description='Сокращает ссылки и выводит количество переходов по ней'
    )
    parser.add_argument('link', help='Введите ссылку:')
    args = parser.parse_args()
    print(args.link)

    parse_link = urlparse(args.link)
    bitlink = f"{parse_link.netloc}{parse_link.path}"
    try:
        if is_bitlink(headers, bitlink):
            print(count_clicks(headers, bitlink))
        else:
            print(shorten_link(headers, args.link))
    except requests.exceptions.HTTPError as error:
        print("неверная ссылка.", error)


if __name__ == "__main__":
    load_dotenv()
    main()
