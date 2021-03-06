import datetime
import csv
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def collect_data(city_code='2398'):
    """This function collects information about discounts from the website https://magnit.ru/promo/
        and write it to csv file"""

    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    ua = UserAgent()

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': ua.random,
    }

    cookies = {
        'mg_geo_id': f'{city_code}'
    }

    response = requests.get(url='https://magnit.ru/promo/', headers=headers, cookies=cookies)

    # with open(f'index.html', 'w', encoding='utf-8') as file:
    #     file.write(response.text)

    with open('index.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    city = soup.find('a', class_='header__contacts-link_city').text.strip()

    cards = soup.find_all('a', class_='card-sale_catalogue')
    # print(city, len(cards))

    with open(f'{city}_{cur_time}.csv', 'w', encoding='cp1251') as file:
        writer = csv.writer(file, delimiter=',')

        writer.writerow(
            (
                'Продукт',
                'Старая цена',
                'Новая цена',
                'Процент скидки',
                'Время акции',
            )
        )

    for card in cards:
        card_title = card.find('div', class_='card-sale__title').text.strip()
        try:
            card_discount = card.find('div', class_='card-sale__discount')
        except AttributeError:
            continue
        card_price_old_integer = card.find('div', class_='label__price_old').find('span', class_='label__price-integer').text.strip()
        card_price_old_decimal = card.find('div', class_='label__price_old').find('span', class_='label__price-decimal').text.strip()
        card_old_price = f'{card_price_old_integer}.{card_price_old_decimal}'

        card_price_integer = card.find('div', class_='label__price_new').find('span', class_='label__price-integer').text.strip()
        card_price_decimal = card.find('div', class_='label__price_new').find('span', class_='label__price-decimal').text.strip()
        card_price = f'{card_price_integer}.{card_price_decimal}'

        card_sale_date = card.find('div', class_='card-sale__date').text.strip().replace('\n', ' ')
        # print(card_sale_date)

        with open(f'{city}_{cur_time}.csv', 'a',  encoding='cp1251') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(
                (
                    card_title,
                    card_old_price,
                    card_price,
                    card_discount,
                    card_sale_date,
                )
            )

    print(f'Файл {city}_{cur_time} успешно записан!')


def main():
    collect_data(city_code='2398')


if __name__ == '__main__':
    main()
