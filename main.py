import requests
import time
from bs4 import BeautifulSoup
from requests_html import HTMLSession

import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import httplib2

import json
from datetime import datetime
import pytz

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os

# test_mode = True
test_mode = False


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-features=NetworkService")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])


chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument("window-size=1200,1000")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')

# ------------------------------Изменить переменные перед деплоем-----------------------------------------

spreadsheet_id ='1dba0Xik4GJKlZvM8o2gUapNu95drAZShtrs9MNSYWPA'
if test_mode:
    driver = webdriver.Chrome(executable_path="drivers\chromedriver.exe", options=chrome_options)
else:
    driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver", options=chrome_options)


to_json = {
  "type": "service_account",
  "project_id": "sstesting",
  "private_key_id": "1e1d26c21d2b468a0400d0927012ab00e83c644d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCHA8TW+716rtkn\n6mW5w4sPHjlDdcetJoDnZHdu85fVbZsN5M3sDrxL5J7GjZv1Aaegw15xRg+0LDXP\n8lFuFgqmH+uulAPyhv0Se44N6Doce9BjiSJZLkpgvJGEEBeZKRbshzLotrDwJ9Y/\nWufG8bW8scoxbvER+39z5yxmhZqJWmy7UIbLTfo6HENmB2n4oZjctY04dIjN9z2M\nfqc8al+SAJ7qi6NrdwZMZFuDroy+z0BzJbvkrmD0PTSC4hGqiw2prTjLFR4dp1Vv\ni2Rnxk+om6OnK3nsBKoro8YXApYTuqBLJ4zdWJF7KrTg3PHb8thvbZsUyR+aLrA/\nGsYJvzx1AgMBAAECggEAA3FGKJEcoK8qnEjutRDWT9lebmjnYXPU35GBNhQB8BAu\nXulRks5BYNIAdmGP82xKYN/6XXsC1X43FQlBqEPpm5i+wqHFg/6LH1iFI7ejG6zQ\ngGkztgBnJxZHw41BfMc+bWN5GdPmqQjq/oyL0lfBYYFK/X2tqd62vjbLvAV2DkB1\nf/tAUbjS8LqNlSAVozKlx7ze7Z2WzrvVE0wKXQC5wseG9iBffmxbCnd/B50U8XyH\n8xpXPrVejGOLxpDRuEOd3CsFMGlrPoN6YnyyC86DJwav3FyWXkoqNJH0yH2r0kAg\n5YA2iOi2K6xvzmrOtaqJbowITK1J0QgbUgkLOyL8dQKBgQC8l1/s9vYGJPSuhYkJ\nSJ6KuR7GgRNxJu0dVZklgT16DrFNEHOr0jIiNauTnulbyJVuXcsrkhHjgM0KdqYe\nxxiM67LbeKzdTiNfIeyh6GHz2J+FsHDRRiwEp1jHhRbymx3gzavBH5WgTPA5aZ31\nchg8qaJl+24IN/ZbyRkn2j0D/wKBgQC3Rf0eC+8P4XM3KrG8kLcSEC+RyYfw19AX\ndk3jntHHGgQjLbDEdecPeNd/kMx1qY1m5fhO5eWuW/vb5de2DfxdiehiniYfbEiJ\nE2Qnr98UVoU/95RmVJFU+Sk8ZR2wC7GPmEbvkl4fiqtRgsubDtB7byno2WFzQXJW\n4/MF4B3viwKBgCHd6TsLqmi2ED6a+l3xbY8p6U3qdgxW2jPvYD4s9FZL9ykIsE0F\nxT0BeFtdKTjzT2pva4HajF3Xjnq3jeNvC4ia9xaUmC5xzsZRuEXnDlgU6ai/Y7Mh\nL9xyFO5XhyRwGLB7HsHioyMTTfxxbA1cvN9/8wrvWPYe3p3jAiJ2/YgPAoGBAJ3/\nrXYgzakAMKbHnNC2Zc0hvRDPD+3278O6Tu3DtpASAq0dL74+8sLo58dm2o05bdje\nu1GxanAFhryNioi9x+oQARI7yxvd6y6ZVAfO29+Zs2hxFTOfBmeeIgmaFpz1h88G\ndWkF4zUIBCfSPZtgiyVOsW+3MAb/zgXQoGtZShV/AoGBAI4ckDle8OxzcQQuScMh\ndbOhg0rBRiqCmVUC9v40ISO/Nu0+9YVTV5gtm3oGJMIQ5okVZalBGNjq0At1GcqK\np7YFNcUkdgjZhLzldp6dqgC5HhX0HOqLZf/CTxMu6CyudxM5EyDsv0eeyis7T6kW\nDKMqPUxwmag4ekgJYzPmidMg\n-----END PRIVATE KEY-----\n",
  "client_email": "account@sstesting.iam.gserviceaccount.com",
  "client_id": "109287569938384590418",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/account%40sstesting.iam.gserviceaccount.com"
}

with open('test.json', 'w') as f:
    f.write(json.dumps(to_json))
CREDENTIALS_FILE = 'test.json'


credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

spreadsheet_id ='1dba0Xik4GJKlZvM8o2gUapNu95drAZShtrs9MNSYWPA'


def get_gs_vals(adress) -> list([]):
    val = service.spreadsheets().values().get(   
        spreadsheetId=spreadsheet_id,
                range=adress,
                majorDimension="ROWS",
        ).execute()

    return val['values'] 


def send__to_gs(val, adress):
    service.spreadsheets().values().batchUpdate(   
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {'range':"Калькуляторы!"+adress,
                "majorDimension": "ROWS",
                "values": [[val]]}
            ]
            }
        ).execute()


def get_adresses(adress):
    l = get_gs_vals(adress)
    dic = {}
    for row in l:
        if len(row) != 1:
            dic[row[0]] = row[1]

    return dic


def get_cur_time():
    print('Работает get cur time')
    moscow_time = str(datetime.now(pytz.timezone('Europe/Moscow')))[:19]
    return moscow_time


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
                min = data[row]['adv']['minSingleTransAmount']
                max = data[0]['adv']['maxSingleTransAmount']

                # print(f"{row} Ник: {nickname}")
                # print(f"Цена: {price}")
                # print(f"Кол-во сделок: {month_orders}")
                # print(f"% Успешных: {success_orders}")
                # print(f"Лимит {fiat}: {data[row]['adv']['minSingleTransAmount']} - {data[0]['adv']['maxSingleTransAmount']}")
                # print(f"Сумма {coin}: {data[row]['adv']['surplusAmount']}")
                # print(f"Способы оплаты: {trade_types}")
                
                # print(data[row]['adv']['tradeMethods'])
                if payment != '':
                    if payment in trade_types and float(month_orders) > orders_count and float(success_orders) > success_rate:
                        # and float(min) <= float(amount) <= float(max)
                        # print(f"{row} Ник: {nickname}")
                        # print(f"Цена: {price}")
                        # print(f"Кол-во сделок: {month_orders}")
                        # print(f"% Успешных: {success_orders}")
                        # print(f"Лимит {fiat}: {data[row]['adv']['minSingleTransAmount']} - {data[0]['adv']['maxSingleTransAmount']}")
                        # print(f"Сумма {coin}: {data[row]['adv']['surplusAmount']}")
                        # print(f"Способы оплаты: {trade_types}")
                        # print('---')
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
        l = s.post(log_url, data=payload) # для аутентификации
        print(l.status_code)
        print(l.text)
        r = s.post(data_url, json=payload2, headers=headers)
        # print(r.status_code)
        
        if r.status_code == 200:
            data = r.json()
            price = data['elements'][1]['value']
            price = price.replace(' UZS', '').replace(' ', '').replace('.', ',')
        else:
            print(f'Курс QIWI RUB/UZS не найден')
            print(r.status_code)
            print(r.text)
            return ''
    
    print(f'Курс QIWI RUB/UZS = {price}')

    return price


# def get_garantex():
#     print('-'*50)
#     print('Ищем курс Garantex RUB/USDT')
#     url = 'https://garantex.io/trading/usdtrub'

#     session = HTMLSession()
#     r = session.get(url)
#     r.html.render(sleep=1)
#     page = r.html

#     soup = BeautifulSoup(r.html.raw_html, "html.parser")

#     table = soup.find('tbody', {'class': 'table table-hover usdtrub_bid bids'})
#     row = table.findAll('tr')[0]
#     price = row.attrs['data-price']
#     price = price.replace('.', ',')

#     print(f'Курс Garantex RUB/USDT = {price}')

#     return price


def get_garantex():
    print('Run Garantex')
    driver.get('https://garantex.io/trading/usdtrub')
    print('Перешли на сайт')
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[@class = 'btn btn-success']")))
        driver.find_element(By.XPATH, "//a[@class = 'btn btn-success']").click()
    except:
        print('cookies are not acceptable')
    print('Проверили куки')

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//tbody[@class='table table-hover usdtrub_bid bids']")))
    except:
        pass
    print('дождались')
    tr = driver.find_element(By.XPATH, "//tbody[@class='table table-hover usdtrub_bid bids']").find_elements(By.TAG_NAME, "tr")
    price = tr[0].get_attribute('data-price')
    price = price.replace('.', ',')
    print(f'Garantex RUB/USDT: {price}')

    return price


def main():
    
    st = time.time()
    adresses_table_adress = get_gs_vals('Z1')[0][0]
    adresses = get_adresses(adresses_table_adress)
    
    try:
        send__to_gs(get_garantex(), adresses['Турция Garantex'])
    except:
        time.sleep(2)
        send__to_gs(get_garantex(), adresses['Турция Garantex'])
    finally:
        driver.close()
        driver.quit()

    try:
        mts = get_mts()
        send__to_gs(mts, adresses['MTC'])
    except:
        print('Не удалось отправить МТС')

    try:
        send__to_gs(get_p2p(trade_type='SELL', fiat='RUB', payment='Tinkoff', amount='300000'), adresses['Тиньк USDT/RUB P2P'])
    except Exception as E:
        print('Не удалось отправить тиньк USDT')
        print(E)
    
    try:
        send__to_gs(get_paysend(), adresses['Paysend RUB/UZS'])
    except:
        time.sleep(3)
        send__to_gs(get_paysend(), adresses['Paysend RUB/UZS'])

    try:
        send__to_gs(get_p2p(trade_type='BUY', fiat='UZS', payment='Paysend.com', amount=get_gs_vals(adresses['Paysend Объем'])[0][0]), adresses['Paysend USDT/UZS'])
    except:
        time.sleep(2)
        send__to_gs(get_p2p(trade_type='BUY', fiat='UZS', payment='Paysend.com', amount=get_gs_vals(adresses['Paysend Объем'])[0][0]), adresses['Paysend USDT/UZS'])
        
    try:
        send__to_gs(get_p2p(trade_type='BUY', fiat='UZS', payment='Uzbek National Bank', amount=get_gs_vals(adresses['UzbekNationalBank USDT/UZS Объем'])[0][0]), adresses['UzbekNationalBank USDT/UZS'])
    except:
        time.sleep(2)
        send__to_gs(get_p2p(trade_type='BUY', fiat='UZS', payment='Uzbek National Bank', amount=get_gs_vals(adresses['UzbekNationalBank USDT/UZS Объем'])[0][0]), adresses['UzbekNationalBank USDT/UZS'])
        
    try:
        send__to_gs(get_p2p(trade_type='BUY', fiat='UZS', payment='', amount=get_gs_vals(adresses['Solid USDT/UZS Объем'])[0][0]), adresses['Solid USDT/UZS'])
    except:
        time.sleep(2)
        send__to_gs(get_p2p(trade_type='BUY', fiat='UZS', payment='', amount=get_gs_vals(adresses['Solid USDT/UZS Объем'])[0][0]), adresses['Solid USDT/UZS'])

    try:
        send__to_gs(get_p2p(trade_type='BUY', fiat='UZS', payment='SalamPay', amount= get_gs_vals(adresses['SalamPay USDT/UZS Объем'])[0][0]), adresses['SalamPay USDT/UZS'])
    except:
        time.sleep(2)
        send__to_gs(get_p2p(trade_type='BUY', fiat='UZS', payment='SalamPay', amount= get_gs_vals(adresses['SalamPay USDT/UZS Объем'])[0][0]), adresses['SalamPay USDT/UZS'])
    
    try:
        send__to_gs(get_p2p(trade_type='SELL', fiat='RUB', payment='RosBank', amount='300000'), adresses['Турция p2p Rosbank'])
    except:
        time.sleep(2)
        send__to_gs(get_p2p(trade_type='SELL', fiat='RUB', payment='RosBank', amount='300000'), adresses['Турция p2p Rosbank'])
    
    try:
        send__to_gs(get_korona_pay(), adresses['Турция Корона'])
    except:
        time.sleep(2)
        send__to_gs(get_korona_pay(), adresses['Турция Корона'])


    try:
        send__to_gs(get_moex('USD'), adresses['Мосбиржа USD'])
    except:
        time.sleep(2)
        send__to_gs(get_moex('USD'), adresses['Мосбиржа USD'])

    try:
        send__to_gs(get_moex('EUR'), adresses['Мосбиржа EUR'])
    except:
        time.sleep(2)
        send__to_gs(get_moex('EUR'), adresses['Мосбиржа EUR'])

    try:
        send__to_gs(get_cur_time(), adresses['Время обновления'])
    except:
        time.sleep(2)
        print('Ошибка кар тайм')
        send__to_gs(get_cur_time(), adresses['Время обновления'])
        
    try:
        send__to_gs(get_mercuryo('USD'), adresses['Mercuryo USD/BUSD'])
    except:
        time.sleep(2)
        send__to_gs(get_mercuryo('USD'), adresses['Mercuryo USD/BUSD'])

    try:
        send__to_gs(get_mercuryo('EUR'), adresses['Mercuryo EUR/BUSD'])
    except:
        time.sleep(2)
        send__to_gs(get_mercuryo('EUR'), adresses['Mercuryo EUR/BUSD'])


    print(f'\nОтработали за {round(time.time() - st, 2)} секунд(ы)')


if __name__ == '__main__':
    main()
    