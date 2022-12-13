'''
Скрапер озона
'''

import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


PAGE_ADRESS ='https://www.ozon.ru/category/smartfony-15502/?page={}&sorting=rating'
NAME_XPATH = "//h1"
LINK_XPATH = "//a[contains(@href, 'product') and contains(@href,'smartfon')"\
    " and not(contains(@href,'advert'))]"
ITEM_XPATH = "//span[contains(text(),'{}')]/../following-sibling::dd"
ITEM_DIC = {'os':'Операционная', 'ver':'Версия'}

#Web-driver parameters
serv = Service(ChromeDriverManager().install())
options = Options()
options.headless = False
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--enable-javascript')
default_driver = webdriver.Chrome(service=serv, options = options)


class PageError(Exception):
    '''
    Page Error
    '''

class BypassError(Exception):
    '''
    Failed to bypass anti-bot protection
    '''

class RepeaterError(Exception):
    '''
    Repeater Error
    '''



def repeater(payload):
    '''
    Repeat procedure in case of exception, raise last exception encountered too much of them
    Raises:
        RepeaterError: if somehow value of err_count got more than 5 without changing last_exception
        pretty much impossible, but...
    '''
    def chamber(*args, driver, **kwargs):
        err_count = 0
        last_exception = RepeaterError('Error in handling errors by repeater decorator')
        while True:
            if err_count >5:
                raise last_exception
            try:
                ret = payload(*args, driver = driver, **kwargs )
            except Exception as ex:
                driver.refresh()
                err_count += 1
                last_exception = ex
            else:
                return ret

    return chamber

def drive(passenger):
    '''
    Load unique web driver instance for decorated procedure
    '''
    def wrapper(*args, **kwargs):
        driver = webdriver.Chrome(service = serv, options = options)
        ret = passenger(driver = driver, *args, **kwargs )
        driver.quit()
        return ret
    return wrapper

def err_catcher(page, driver = default_driver):
    '''
    Chek page for error message either from Ozon or Cloudflare
    Raises:
        PageError: raises when loaded Ozon error page
        BypassError: raises when cloudflare CAPTCHA is loaded
    '''
    driver.get(page)
    if driver.find_elements(By.XPATH,"//h2[@class='c']"):
        if 'Произошла ошибка' in driver.find_element(By.XPATH,"//h2[@class='c']").text:
            raise PageError('Driver got error page')
    elif 'Cloudflare' in driver.page_source:
        raise BypassError('Scraper failed to bypass cloudflare')

@repeater
def scroll(breaking_line: str, driver: webdriver):
    '''
    Scroll page until target str is loaded
    Parameters:
            breaking_line (str): Target str
            driver: selenium.webdriver object
    Raises:
        PageError('Cant load whole page'): after 5 tries of scrolling to end raises exception
    '''
    tries = 0
    while True:
        if tries>5:
            raise PageError('Cant load whole page')
        tries += 1
        #прокручивает вниз
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        if str(breaking_line) in driver.page_source:
            break
        #немного сдвигает наверх (озон не всегда прогружается полностью если крутить только вниз)
        driver.execute_script('window.scrollBy(0,-250)')
        time.sleep(2)


@drive
@repeater
def __get_page__(pag_num = 1, driver = default_driver):
    '''
    Get all links with set XPATH and from loaded page, remove GET-reques garbage fron end of link
        Parameters:
            pag_num (int): number of page to load
            driver: selenium.webdriver object
        Return:
            links_text list[str]: list of links in str
    '''
    page = PAGE_ADRESS.format(pag_num)
    err_catcher(page, driver = driver)
    scroll(breaking_line = 'Все права защищены.', driver = driver)
    links= driver.find_elements(By.XPATH, LINK_XPATH)
    links_text = [link.get_attribute('href').split('?')[0] for link in links]
    return links_text

@drive
@repeater
def read_page(page, driver = default_driver):
    '''
    Get valuable data from target page
        Parameters:
            page (str): link to page
            driver: selenium.webdriver object
        Return:
            ret (dic): dictionary with data
                {
                    'name': name of item,
                    'os': name of OS,
                    'ver': version of OS
                }
    '''
    err_catcher(page, driver)
    scroll(breaking_line = 'Отзывы и вопросы о товаре', driver = driver)
    ret = {}
    for key, item in ITEM_DIC.items():
        read = driver.find_element(By.XPATH, ITEM_XPATH.format(item)).text
        ret[key] = read
    ret['name'] = driver.find_element(By.XPATH, NAME_XPATH).text
    return ret

def get_pages(amount):
    '''
    Iterate __get_page__ till set amount of links is scraped
        Parameters:
            amount (int): amount of links to scrap
        Return:
            page_set (list): list of links
    '''
    page_set = set()
    page = 1

    while True:
        sub = set(__get_page__(pag_num = page))
        for item in sub:
            page_set.add(item)
            l = len(page_set)
            print(f'Scraped links: {l:>10} out of {amount}', end ='\r')
            if l>=amount:
                print()
                return list(page_set)
        page +=1


def scrap_em(num):
    '''
    Scraps data about n first items in top
        Parameters:
            num (int): number of items to scrap
        Return:
            oses (list[dict]): list of dictionaries
                {
                    'name': name of item,
                    'os': name of OS,
                    'ver': version of OS
                }
    '''
    oses= []
    tar_list = get_pages(num)
    err_list = []
    for index, item in enumerate(tar_list):
        print(f'{index}: Scraping {item}')
        try:
            time.sleep(2)
            oses.append(read_page(page = item))
        except Exception as ex:
            print('Got error')
            err_list.append(f'Error at item number {index}: {item} \n {ex}')
    print(f'Successfully sacraped {len(oses)}/{num} with {len(err_list)} unevaded errors')
    if len(err_list) >0:
        print('Log of unevaded errors:')
        for item in err_list:
            print(item)
    return oses

if __name__ == '__main__':
    with open('test_dump.json', 'w', encoding = 'UTF-8') as file:
        file.write(json.dumps(scrap_em(10)))

default_driver.quit()
