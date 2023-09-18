from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json

def security_page():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("prefs", {"ignore_certificate_errors": True})

    s = Service(
        executable_path="D:\\Repos\\VScode\\Scraping_sportmaster\\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        '''
    })

    return driver


def get_page():
    count=1
    while True:
        print(count)
        url = f"https://www.sportmaster.ru/catalog/muzhskaya_obuv/vsya_muzhskaya_obuv/?f-prod_kind=prod_kind_krossovki_i_kedy&f-kind_of_product=kind_of_product_krossovki&f-ra=size_44,size_44d5&f-promotion:globalpromo=true&watched=35,0&page={count}"
        count = count + 1
        yield url


def get_data():
    driver = security_page()
    page_list = get_page()
    result_data = []
    try:
        for url in page_list:
            driver.get(url=url)
            time.sleep(2)
            names = driver.find_element(By.CSS_SELECTOR, '[class="sm-product-grid sm-product-grid--size-xs"]').find_elements(By.CSS_SELECTOR, '.sm-link.sm-link_black')
            prices_new =driver.find_element(By.CSS_SELECTOR, '[class="sm-product-grid sm-product-grid--size-xs"]').find_elements(By.CSS_SELECTOR, '.sm-amount.price__retail.sm-amount--default')
            prices_old = driver.find_element(By.CSS_SELECTOR, '[class="sm-product-grid sm-product-grid--size-xs"]').find_elements(By.CSS_SELECTOR, '.sm-amount.price__catalog.sm-amount--old')
            links = driver.find_element(By.CSS_SELECTOR, '[class="sm-product-grid sm-product-grid--size-xs"]').find_elements(By.CSS_SELECTOR, '[data-selenium="product-name"]')


            for name,price_new,price_old,link in zip(names,prices_new,prices_old,links):
                name = name.text.strip()
                price_new = price_new.text.strip()
                price_old = price_old.text.strip()
                link = link.get_attribute('href')

                
            
                result_data.append({
                    'name': name,
                    'price_new': price_new,
                    'price_old': price_old,
                    'link': link,
                })
        


    except Exception as ex:
        print(ex)

    finally:
        with open("result_data_sneakers.json", "w") as file:
            json.dump(result_data, file, indent=4)


        driver.close()
        driver.quit()


def main():
    get_data()


if __name__ == "__main__":
    main()
