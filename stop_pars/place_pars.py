from selenium.webdriver.common.proxy import Proxy, ProxyType

import time

from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

from datetime import datetime


# need_name -- название нужного ресторана
need_name = 'Дагестанская Лавка'

now = datetime.now()

# настройки парсинга
user_agents = UserAgent()

# s = Service('stop_pars/chromedriver.exe')
s = Service('C:/Users/Nastya/PycharmProjects/PARS_dag/stop_pars/chromedriver.exe')

url = 'https://eda.yandex.ru/'
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument(f'user-agent={user_agents.random}')
options.add_argument("--incognito")
options.add_argument("--window-size=1500,1500")
options.add_argument("--disable-blink-features=AutomationControlled")

def restaurant_search(text):
    """Парсит сайт яндекс еды.

        driver -- при запуске через VPS нужно убрать подключение к proxy

        Стоит тайминг для прогрузки страницы.
        Парсинг медленно специально, чтобы страница успела прогрузиться.

        В конце запись файла == text
    """
    # login = login_proxy
    # password = password_proxy
    #
    # proxy = Proxy()
    # proxy.proxy_type = ProxyType.MANUAL
    # proxy.http_proxy = f"{login}:{password}@149.126.218.116:8000"
    # proxy.ssl_proxy = f"{login}:{password}@149.126.218.116:8000"
    #
    # capabilities = webdriver.DesiredCapabilities.CHROME
    # proxy.add_to_capabilities(capabilities)
    # time.sleep(2)

    # driver = webdriver.Chrome(service=s, options=options, desired_capabilities=capabilities)

    driver = webdriver.Chrome(service=s, options=options)

    driver.delete_all_cookies()
    print(f'...Start парсинг место выдачи ресторана по адресу:  {text}')

    driver.save_screenshot('scrin/1_место_открытие.png')

    try:
        driver.get(url='https://eda.yandex.ru/')
        time.sleep(15)
        driver.save_screenshot('scrin/2_место_скрин_страницы.png')
        print('open modalsls')

        driver.find_element(By.CSS_SELECTOR,
                            "span.DesktopAddressButton_address").click()

        time.sleep(1)
        driver.save_screenshot('scrin/3_место_скрин_модалки.png')

        time.sleep(2)
        print('search address')
        driver.save_screenshot('scrin/4_место_скрин ввод адреса.png')
        home_1 = driver.find_element(By.CSS_SELECTOR,
                                     "input.AppAddressInput_addressInput.AppAddressInput_modalStyle")

        time.sleep(7)

        direction_text = text
        for ch in direction_text:
            home_1.send_keys(ch)
            time.sleep(0.1)
        print('...Адрес введен:', text)

        driver.save_screenshot('scrin/5_место - адрес введен.png')
        time.sleep(6)

        print('клик по пикселям адреса')

        driver.save_screenshot('scrin/6_место клик по пикселям адреса.png')
        try:
            print('пробуем нажать на кнопку ОК')
            home_1.find_element('xpath', '/html/body/div[4]/div/div/div/div/div[1]/div[2]/button/span').click()

            driver.save_screenshot('scrin/7_место скрин Нажали на ок кнопку.png')
            print('Нажали на ок кнопку')

        except Exception as ex:
            print('Не вышло первый раз нажать ОК')


        driver.save_screenshot('scrin/8_место-скролл попытка.png')
        time.sleep(2)

        # top_res = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div/div[9]/div/div/div")
        top_res = driver.find_element(By.CLASS_NAME, 'PlaceList_flexByHeight')
        time.sleep(5)
        scroll_origin = ScrollOrigin.from_element(top_res)
        print('Начинаем скрол')
        all_rest = []
        for _ in range(85):
            time.sleep(0.3)
            ActionChains(driver).scroll_from_origin(scroll_origin, 0, 200).perform()

            # try:
            #     iframe = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div/button[1]")
            #     iframe.click()
            #     time.sleep(0.5)
            # except Exception:
            #     print('кнопка не нашлась')

            try:
                res_names = driver.find_elements(By.CLASS_NAME, "NewPlaceItem_title")
                for item in res_names:
                    if item.text.split('\n') not in all_rest:
                        all_rest.append(item.text.split('\n'))
            except Exception as ex:
                print(ex)

        print(all_rest)
        driver.save_screenshot('scrin/9_место-скролл.png')
        text_file = text.strip().replace(',', '_').replace('/', '_').replace(' ', '')

        with open(f'{text_file}.txt', 'w', encoding='utf-8') as file:
            for i in all_rest:
                for name_rest in i:
                    file.write(f'{name_rest}\n')

            print('...записали файл')
        print('...парсинг адреса закончен <-')

    except Exception as ex:
        actions = ActionChains(driver)
        actions.move_by_offset(750, 750).perform()
        time.sleep(2)
        actions.double_click().perform()
        time.sleep(2)
        driver.save_screenshot('scrin/2_err.png')

        time.sleep(2)
        print(ex)

    finally:
        driver.close()
        driver.quit()

# restaurant_search('Москва, улица Поликарпова, 23Ак14\n')
