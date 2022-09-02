from selenium import webdriver
from time import sleep
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import httplib2
import os
import json
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

test_mode = True
# test_mode = False

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
    driver = webdriver.Chrome(executable_path="drivers\chromedriver_linux", options=chrome_options)
# spreadsheet_id = '1TCW2UXCQImCHOPv-Dq_B7JA7lFkW-G_WSpUWp8tqNlU'
# ------------------------------Изменить переменные перед деплоем-----------------------------------------

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

get_qiwi_url = 'https://qiwi.com/payment/form/38489'
qiwi_login_url = 'https://qiwi.com/'



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
                {'range':adress,
                "majorDimension": "ROWS",
                "values": [[val]]}]
            }
        ).execute()


def get_adresses(adress):
    l = get_gs_vals(adress)
    # print(l)
    dic = {}
    for row in l:
        if len(row) != 1:
            dic[row[0]] = row[1]

    return dic


def get_qiwi():
    # qiwi_login()
    print('Работает get qiwi')
    driver.get(url=get_qiwi_url)

    sleep(3)
    card = driver.find_elements(by=By.XPATH, value="//input[contains(@class, 'input')]")[0]
    print('нашли card')
    amount = driver.find_elements(by=By.XPATH, value="//input[contains(@class, 'input')]")[1]
    print('нашли amount')

    card.send_keys('8600572959157509')
    print('отправили карту')

    sleep(2)
    amount.send_keys('100')

    sleep(3)
    res = driver.find_element(by=By.XPATH, value="//div[contains(text(), 'UZS')]").text
    res = float(float(res[:-4].replace(' ', '')) / 100)
    print(res)
    return res


def qiwi_login():
    print('Работает qiwi login')
    driver.get(url=qiwi_login_url)
    sleep(5)
    driver.find_element(by=By.CLASS_NAME, value='css-1r1bp18').click()
    sleep(2)
    # driver.get_screenshot_as_file('artem_p2p\\selenium-binance4\\s_login.png')
    btns = driver.find_elements(by=By.XPATH, value="//button")
    for i in btns:
        if i.text == 'У меня есть кошелек':
            # driver.get_screenshot_as_file('artem_p2p\\selenium-binance4\\all_btns.png')
            i.click()
            break

    time.sleep(5)
    # driver.get_screenshot_as_file('artem_p2p\\selenium-binance4\\afterClick.png')
    phone = driver.find_element(by=By.XPATH, value="//input[@name='username']")
    phone.send_keys('9173408585')
    pas = driver.find_element(by=By.XPATH, value="//input[@name='password']")
    pas.send_keys('bit123biT')
    print("отправили лог пароль")
    btn = driver.find_element(by=By.XPATH, value="//button[@type='submit']")
    actions = ActionChains(driver)
    actions.move_to_element(btn)
    actions.perform()
    print('нажали на логин')
    btn.click()
    sleep(3)

try:
    adresses_table_adress = get_gs_vals('Калькуляторы!Z1')[0][0]
    adresses = get_adresses(adresses_table_adress)
    # print(adresses)
    qiwi_login()
    send__to_gs(get_qiwi(), 'Калькуляторы!' + adresses['Qiwi'])
except:
    # driver = webdriver.Chrome(executable_path="drivers\chromedriver_linux", options=chrome_options)
    qiwi_login()
    send__to_gs(get_qiwi(), 'Калькуляторы!' + adresses['Qiwi'])
