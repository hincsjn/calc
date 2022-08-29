import requests
import time
from bs4 import BeautifulSoup
from requests_html import HTMLSession


def get_p2p(trade_type='SELL', coin='USDT', fiat='RUB', payment='Tinkoff', amount='300000', orders_count=100, success_rate=0.95):
    print('-'*50)
    print(f'Ищем курс Binance P2P для {fiat}/{coin}, {payment}, {amount}')
    
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    pages=100
    
    price = ''

    B = False
    for page in range(1, pages):
        if B:
            break
        try:
            payload = {
                "asset": coin,
                "countries": [],
                "fiat": fiat,
                "page": page,
                "payTypes": [],
                "publisherType": None,
                "rows": 10,
                "tradeType": trade_type,
                "transAmount":  amount
            }

            data = requests.post(url, json=payload).json()['data']

            for row in range(10):
                nickname = data[row]['advertiser']['nickName']
                price = data[row]['adv']['price']
                month_orders = data[row]['advertiser']['monthOrderCount']
                success_orders = data[row]['advertiser']['monthFinishRate']
                trade_types = [i['tradeMethodName'] for i in data[row]['adv']['tradeMethods']]
                
                # print(data[row]['adv']['tradeMethods'])
                if payment != '':
                    if payment in trade_types and float(month_orders) > orders_count and float(success_orders) > success_rate:
                        # print(f"{row} Ник: {nickname}")
                        # print(f"Цена: {price}")
                        # print(f"Кол-во сделок: {month_orders}")
                        # print(f"% Успешных: {success_orders}")
                        # print(f"Лимит {fiat}: {data[row]['adv']['minSingleTransAmount']} - {data[0]['adv']['maxSingleTransAmount']}")
                        # print(f"Сумма {coin}: {data[row]['adv']['surplusAmount']}")
                        # print(f"Способы оплаты: {trade_types}")
                        B = True
                        break
                else:
                    if float(month_orders) > orders_count and float(success_orders) > success_rate:
                        # print(f"{row} Ник: {nickname}")
                        # print(f"Цена: {price}")
                        # print(f"Кол-во сделок: {month_orders}")
                        # print(f"% Успешных: {success_orders}")
                        # print(f"Лимит {fiat}: {data[row]['adv']['minSingleTransAmount']} - {data[0]['adv']['maxSingleTransAmount']}")
                        # print(f"Сумма {coin}: {data[row]['adv']['surplusAmount']}")
                        # print(f"Способы оплаты: {trade_types}")
                        B = True
                        break

        except Exception as E:
            print(f'Стопнулись на {page}')
            print(E)
            break

    if price == '':
        print('-'*50, 'Не нашли(')
    else:
        if '.' in price:
            price = price.replace('.', ',')
        
        print(f'Курс Binance P2P для {fiat}/{coin}, {payment} = {price}')
        return price


def get_mts():
    print('-'*50)
    print(f'Ищем курс МТС')
    price = ''
    r = requests.get(url='https://core.unired.uz/api/open/rate')
    # print(r.status_code)
    price = r.json()['result'][2]['rate']['buy']

    price = str(price)
    if '.' in price:
        price = price.replace('.', ',')
    print(f'Курс МТС = {price}')

    return price


def get_moex(cur):
    print('-'*50)
    print(f'Ищем курс мосбиржи для RUB/{cur}')
    url = f'https://www.moex.com/ru/derivatives/currency-rate.aspx?currency={cur}_RUB'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    res = soup.find_all('span', id='ctl00_PageContent_tbxCurrentRate')[0].text
    price = res.split()[2]
    print(f'Курс мосбиржи для RUB/{cur} = {price}')

    return price


def get_korona_pay():
    print('-'*50)
    print('Ищем курс KoronaPay Turkey')
    url = f'https://koronapay.com/transfers/online/api/transfers/tariffs?sendingCountryId=RUS&sendingCurrencyId=810&receivingCountryId=TUR&receivingCurrencyId=840&paymentMethod=debitCard&receivingAmount=10000&receivingMethod=cash&paidNotificationEnabled=true'

    proxy = 'http://28YBDm5P:5sUPdD52@212.193.188.96:50348'

    proxies = {
        'http': proxy,
        'https': proxy
    }

    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    r = requests.get(url, proxies=proxies, headers=headers, timeout=10)
    price = r.json()[0]['exchangeRate']
    price = str(price).replace('.', ',')
    print(f'Курс KoronaPay RUB/USD = {price}')

    return price


def get_mercuryo(cur):
    print('-'*50)
    print(f'Ищем курс Mercuryo для {cur}/BUSD')

    url = f'https://api.mercuryo.io/v1.6/widget/buy/rate?from={cur}&to=USDT&amount=1000.00&widget_id=3be288da-e82d-4547-bc4a-32fbbe4714a7&is_total=true'

    proxy = 'http://28YBDm5P:5sUPdD52@212.193.188.96:50348'

    proxies = {
        'http': proxy,
        'https': proxy
    }

    r = requests.get(url, proxies=proxies, timeout=10)

    price = r.json()['data']['amount']
    price = str(float(price) / 1000).replace('.', ',')
    print(f'Курс Mercurio {cur}/BUSD: {price}')

    return price


def get_paysend():
    print('-'*50)
    print('Ищем курс Paysend RUB/UZS')

    r = requests.get('https://paysend.com/ru-ru/zaprosit-dengi/iz-rossii-v-uzbekistan')
    # print(r.status_code)
    soup = BeautifulSoup(r.text, 'lxml')

    res = soup.find('span', {'class':'foo'}).text
    price = res.split(' = ')[-1].split()[0]

    if '.' in price:
        price = price.replace('.', ',')

    print(f'Курс Paysend RUB/UZS = {price}')
    return price


def get_qiwi():
    print('-'*50)
    print('Ищем курс QIWI RUB/UZS')

    proxy = 'http://28YBDm5P:5sUPdD52@212.193.188.96:50348'

    proxies = {
        'http': proxy,
        'https': proxy
    }

    log_url = 'https://qiwi.com/oauth/token'
    payload = {
        'token_type': 'headtail',
        'grant_type': 'password',
        'client_secret': 'P0CGsaulvHy9',
        # 'anonymous_token_head': '3142fc261f0afdcb',
        'client_id': 'web-qw',
        'username': '+79173408585',
        'password': 'bit123biT'
    }

    data_url = 'https://edge.qiwi.com/sinap/api/refs/991ad09a-9d94-481e-8640-eb8be592db38/containers'
    payload2 = {
        'account': "8600572959157509",
        'amount': "100",
        'ccy': "RUB",
        'first_name': "Роберт",
        'last_name': "Гумеров",
        'middle_name': "Русланович",
        'prvId': "38489",
        'wallet': "79173408585",
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'authority': "edge.qiwi.com",
        'accept': "application/vnd.qiwi.v1+json",
        'accept-language': "ru",
        'authorization': "TokenHeadV2 d2ViLXF3OmFkMzA5MWE4ZjhjYTVmOTU=",
        'client-software': "WEB v4.123.0",
        'content-type': "application/json",
        'cookie': "_ga_cid=undefined; uxs_uid=151013c0-fae6-11ec-b0e2-69e9d1cf1987; uxs_mig=1; token-tail=a4e7adcad76a1248; spa_upstream=9d4a3462e8cb1b20294a01cda54e3027; token-tail-web-qw=40f90161ade60abb; auth_ukafokfuabbuzdckyiwlunsh=MDIwfF98X3wIW1ViJApTDF4gJkt1GFNdJVQUJFJ3DWwAYDQEDGIqL2kJUzccS2APdXVXcwdhXn4AAXxEZFEFX3dGTGoLH01pDFgZaXEKAkNLc34fdlYEDCUBXXMcc1p3AWZpBQZifQ==; _ga_info=8^|6^|1661694281558^|false^|185e6b6ebfd2d6e585ef8f8445c613aaa0e576c8b45f46519ff06c93a0ac2efd",
        'origin': "https://qiwi.com",
        'referer': "https://qiwi.com/",
        'sec-ch-ua': "^\^Chromium^^;v=^\^104^^, ^\^"
        }


    with requests.session() as s:
        # l = s.post(log_url, data=payload) # для айтентификации
        r = s.post(data_url, json=payload2, headers=headers)
        if r.status_code == 200:
            data = r.json()
            price = data['elements'][1]['value']
            price = price.replace(' UZS', '').replace(' ', '').replace('.', ',')
        else:
            print(f'Курс QIWI RUB/UZS не найден')
            return ''
    
    print(f'Курс QIWI RUB/UZS = {price}')

    return price


def get_garantex():
    print('-'*50)
    print('Ищем курс Garantex RUB/USDT')
    url = 'https://garantex.io/trading/usdtrub'

    session = HTMLSession()
    r = session.get(url)
    r.html.render(sleep=1)
    page = r.html

    soup = BeautifulSoup(r.html.raw_html, "html.parser")

    table = soup.find('tbody', {'class': 'table table-hover usdtrub_bid bids'})
    row = table.findAll('tr')[0]
    price = row.attrs['data-price']
    price.replace('.', ',')

    print(f'Курс Garantex RUB/USDT = {price}')

    return price


def main():
    
    st = time.time()

    get_mts()
    get_p2p(trade_type='SELL', fiat='RUB', payment='Tinkoff', amount='300000')
    get_paysend()
    get_p2p(trade_type='BUY', fiat='UZS', payment='Uzbek National Bank', amount='8725755')
    get_p2p(trade_type='BUY', fiat='UZS', payment='', amount='8725755')
    get_p2p(trade_type='BUY', fiat='UZS', payment='Paysend.com', amount='8725755')
    get_p2p(trade_type='BUY', fiat='UZS', payment='SalamPay', amount='8725755')
    get_p2p(trade_type='SELL', fiat='RUB', payment='Rosbank', amount='300000')
    get_korona_pay()
    get_moex('USD')
    get_moex('EUR')
    get_mercuryo('USD')
    get_mercuryo('EUR')
    get_qiwi()
    get_garantex()

    print(f'\nОтработали за {round(time.time() - st, 2)} секунд(ы)')


if __name__ == '__main__':
    main()