import requests
from bs4 import BeautifulSoup
from selenium import webdriver
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


# Обрабатывает ошибки DOM дерева
def trade_all(driver, index=0):
    while True:
        all_elem = driver.find_elements_by_xpath(
            "//form[@id='aspnetForm']/div[@class='master_open_content']/"
            "div/div/div[@id='resultTable']/div/"
            "div[@class='purch-reestr-tbl-div']")  # может взять с [index]
        if index >= len(all_elem):
            break
        # TODO: Переключение страниц
        # href_all_elem = WebDriverWait(all_elem, 0.5).until(
        #     EC.element_to_be_clickable((
        #         By.XPATH, "table[@class='es-reestr-tbl its']/tbody/"
        #                   "tr[@class='dotted-botom last']/td/div/"
        #                   "div[@style='display: inline;']/"
        #                   "input[@value='/  Просмотр']"
        #         ))).click()

        # href_all_elem = driver.find_elements_by_xpath(
        #     "table[@class='es-reestr-tbl its']/tbody/"
        #     "tr[@class='dotted-botom last']/td/div/"
        #     "div[@style='display: inline;']/"
        #     "input[@value='/  Просмотр']"
        # )

        # if index >= len(href_all_elem):
        #     break
        yield all_elem[index]  #, href_all_elem[index]
        index += 1


# Обработка текста
def word_processing(data):
    checked = []
    pattern = r".*\n"
    string = re.compile(pattern)
    for reg in data:
        may_be = string.findall(reg)
        negative_facts = ["Рассмотрение", "Завершено", "Завершен(-а)", "Отменено", "Отменен(-а)",
                          "Не", "В", "Подведение", "Опубликован(-а)"]
        if all(l not in may_be[3].replace('\n', '').split()[0] for l in negative_facts):
            checked.append(string.findall(reg))
    return checked


# TODO: сделать ассинхронные запросы
def selenium_parse1(param):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)  # /usr/local/bin
    # driver = webdriver.Firefox()
    driver.get("http://sberbank-ast.ru")
    driver.implicitly_wait(1)  # seconds
    map_table = []
    clear_table = []
    try:
        wait = WebDriverWait(driver, 0.5)
        element_input = wait.until(
            EC.presence_of_element_located((By.ID, "txtUnitedPurchaseSearch")))

        element_input.send_keys(param)
        click_element = driver.find_element_by_id("btnUnitedPurchaseSearch")
        click_element.click()  # Переход
        time.sleep(0.2)
        # print(driver.current_url)
        element_select = driver.find_element_by_xpath("//select[@id='headerPagerSelect']")
        all_options = element_select.find_elements_by_tag_name("option")
        all_options[2].click()  # Выставление 100 значений на странице

        for table in trade_all(driver):
            map_table.append(table.text)

        start_time = time.time()
        reg_table = word_processing(map_table)
        for i in reg_table:
            if i[6] != '\n':
                clear_table.append([i[4], i[0], i[2], i[6], i[-2]])
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
