import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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


def selenium_parse1(param):
    driver = webdriver.Firefox()
    driver.get("http://sberbank-ast.ru")  # /usr/local/bin
    driver.implicitly_wait(0.5)  # seconds
    map_table = []
    try:
        wait = WebDriverWait(driver, 0.2)
        element_input = wait.until(
            EC.presence_of_element_located((By.ID, "txtUnitedPurchaseSearch")))

        element_input.send_keys(param)
        click_element = driver.find_element_by_id("btnUnitedPurchaseSearch")
        click_element.click()
        time.sleep(0.2)
        # print(driver.current_url)
        # TODO: Сделать привязку ссылок, осуществить считывание по всем страницам ,попробовать class="link-button"
        for table in wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, "//form[@id='aspnetForm']/div[@class='master_open_content']/"
                           "div/div/div[@id='resultTable']/div/"
                           "div[@class='purch-reestr-tbl-div']"))):
            map_table.append(table.text)
            # print(len(map_table))
        # page = driver.page_source
        # soup = BeautifulSoup(page, 'html')
        # print(soup)
    finally:
        # print(driver.find_element_by_xpath("//div[@class='default_search_border']").text)
        for table in range(len(map_table)):
            print(map_table[table])
            print('<----------------------------->')
        # print(map_table)
        driver.close()


# pages = set()
# def getlinks(pageUrl):
#     global pages
#     # html = urlopen("http://sberbank-ast.ru" + pageUrl)
#     soup = BeautifulSoup(pageUrl, features="lxml")
#     try:
#         for links in soup.findAll('input', class_='link-button'):
#
#         print(soup.findAll('div', class_='purch-reestr-tbl-div'))
#     except ArithmeticError:
#         print("Warning!")
#     # try:
#     #     print(bsObj.h1.get_text())
#     #     print(bsObj.find(id ="Aw-content-text").findAll("p")[0])
#     #     print(bsObj.find(id="ca-edit").find("span").find("a").attrs['href'])
#     # except AttributeError:
#     #     print("Thi.s page i.s PJi.ssi.ng soPJethi.ng! No worries though!")
#     # for link in bsObj.findAll("a", href=re.compile("^(/wi.ki./)")):
#     #     if 'href' in link.attrs:
#     #         if link.attrs['href'] not in pages:
#     #             newPage = link.attrs['href']
#     #             print("----------------\n" + newPage)
#     #             pages.add(newPage)
#     #             getlinks(newPage)


if __name__ == '__main__':
    selenium_parse1("молоко")
    # tender1("рельсы")
