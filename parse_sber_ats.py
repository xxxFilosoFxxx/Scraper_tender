import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config as cfg
import datetime
import random
import re
import time

random.seed(datetime.datetime.now())


# Не подхоит, так как каждый из 'input' привязан к js
def tender1(param):
    session = requests.Session()
    headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
                "Accept": "text/html,application/xhtml+xml,application/xml;"
                          "q=0.9,image/webp,*/*;q=0.8"})

    sber = "http://sberbank-ast.ru"
    responce = session.get(sber, headers=headers)
    soup = BeautifulSoup(responce.text, 'html.parser')
    # search_form = soup.find_all('input', "default_search_input1")
    search_form = soup.find_all('div', "default_search_border")
    print(search_form)


# Обрабатывает ссылки нужных тендеров
def href_trade_all(driver, index=0):
    href_list = []
    while index < 50:
        href_all_elem = WebDriverWait(driver, 0.5).until(
                EC.presence_of_all_elements_located((
                    By.XPATH, "//form[@id='aspnetForm']/div[@class='master_open_content']/"
                              "div/div/div[@id='resultTable']/div/"
                              "div[@class='purch-reestr-tbl-div']/"
                              "table[@class='es-reestr-tbl its']/tbody/"
                              "tr[@class='dotted-botom last']/td/div[@class='element-in-one-row']")))
        try:
            WebDriverWait(href_all_elem[index], 0.1).until(EC.presence_of_all_elements_located((
                    By.XPATH, "div[@style='display: inline;']/input[@value='Подать заявку']")))
            # TODO: возможно ли ускорить?
            button = WebDriverWait(href_all_elem[index], 0.2).until(EC.element_to_be_clickable((
                By.XPATH, "input[@type='button' and @value='/  Просмотр']")))
            # button = href_all_elem[i].find_element_by_xpath("input[@type='button' and @value='/  Просмотр']")
            driver.execute_script("arguments[0].click();", button)
            driver.switch_to_window(driver.window_handles[-1])
            while str(driver.current_url) == "about:blank":
                pass
            url = str(driver.current_url)
            href_list.append(url)
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
        except StaleElementReferenceException:
            pass
        except TimeoutException:
            pass
        index += 1
    return href_list


# Обрабатывает ошибки DOM дерева
def trade_all(driver, index=0):
    while True:
        all_elem = driver.find_elements_by_xpath(
            "//form[@id='aspnetForm']/div[@class='master_open_content']/"
            "div/div/div[@id='resultTable']/div/"
            "div[@class='purch-reestr-tbl-div']")  # может взять с [index]
        if index >= len(all_elem):
            break
        yield all_elem[index]
        index += 1


# Обработка текста
def word_processing(data):
    checked = []
    pattern = r".*\n"
    string = re.compile(pattern)
    for reg in data:
        may_be = string.findall(reg)
        negative_facts = ["Рассмотрение", "Завершено", "Завершен(-а)", "Отменено", "Отменен(-а)",
                          "Не", "В", "Подведение", "Опубликован(-а)", "Tорговый", "Работа"]
        # true_facts = ["Подача заявок", "Прием заявок"]
        if all(l not in may_be[3].replace('\n', '').split()[0] for l in negative_facts):
            checked.append(string.findall(reg))
    return checked


# TODO: среднеее время на 50 запросов: 80 сек., попробовать ускорить алгоритм
def selenium_parse1(param):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)  # /usr/local/bin
    # driver = webdriver.Firefox()
    # driver.maximize_window()
    # driver.implicitly_wait(20)

    driver.get("http://sberbank-ast.ru")
    driver.implicitly_wait(1)  # seconds
    map_table = []
    href_table = []
    clear_table = []
    try:
        wait = WebDriverWait(driver, 0.5)
        element_input = wait.until(
            EC.presence_of_element_located((By.ID, "txtUnitedPurchaseSearch")))

        element_input.send_keys(param)
        click_element = driver.find_element_by_id("btnUnitedPurchaseSearch")
        click_element.click()  # Переход
        time.sleep(0.2)
        element_select = driver.find_element_by_xpath("//select[@id='headerPagerSelect']")
        all_options = element_select.find_elements_by_tag_name("option")
        all_options[1].click()  # Выставление 50 значений на странице

        start_time = time.time()
        for table in href_trade_all(driver):
            href_table.append(table)

        for table in trade_all(driver):
            map_table.append(table.text)

        reg_table = word_processing(map_table)
        h = 0
        for i in reg_table:
            if i[6] != '\n':
                clear_table.append([i[4], i[0], i[2], i[6], i[-2], href_table[h]])
                h += 1
        print("%f seconds" % (time.time() - start_time))

        # page = driver.page_source
        # soup = BeautifulSoup(page, 'html')
        # print(soup)
    finally:
        for i in range(len(clear_table)):
            print(clear_table[i])
            print('<----------------------------->')
        print(len(clear_table))
        driver.close()


if __name__ == '__main__':
    """Передача аргументов командной строки исполняемой функции"""
    selenium_parse1(param=cfg.SEARCH_KEY)
