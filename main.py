import time

from selenium import webdriver
from selenium.webdriver.common.by import By

money_map = {
    'million': 1_000_000,
    'billion': 1_000_000_000,
    'trillion': 1_000_000_000_000,
}

driver_path = r"D:/chromedriver.exe"
chr_options = webdriver.ChromeOptions()
chr_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(executable_path=driver_path, options=chr_options)

driver.get("http://orteil.dashnet.org/cookieclicker/")
driver.maximize_window()
time.sleep(1)

try:
    got_it = driver.find_element(By.LINK_TEXT, 'Got it!')
    got_it.click()
    time.sleep(1)
except:
    pass

lang = driver.find_element(By.CSS_SELECTOR, "#langSelect-EN")
lang.click()
time.sleep(1)

cookie = driver.find_element(By.ID, "bigCookie")
time.sleep(2)

five_min = time.time() + 60 * 500
timeout = time.time() + 5
while True:
    cookie.click()
    if time.time() > timeout:
        items = driver.find_elements(By.CSS_SELECTOR, "#products .unlocked")
        item_ids = [item.get_attribute('id') for item in items]

        item_prices_elements = driver.find_elements(By.CSS_SELECTOR, "#products .product .price")
        item_prices = []
        for i in item_prices_elements:
            if i.text != "":
                if ('million' or 'billion' or 'trillion') in i.text:
                    item_prices.append(float(i.text.split()[0].strip().replace(',', '')) * money_map[i.text.split()[1]])
                else:
                    item_prices.append(int(i.text.strip().replace(',', '')))

        unlocked_products = {}
        for i in range(len(item_ids)):
            unlocked_products[item_prices[i]] = item_ids[i]

        try:
            cookie_count = int(driver.find_element(By.CSS_SELECTOR, "#cookies").text.replace(',', '').split()[0])
        except ValueError:
            cookie_count = driver.find_element(By.CSS_SELECTOR, "#cookies")
            cookie_count = int(cookie_count.text.replace(',', '').split()[0] * money_map[cookie_count.text.split()[1]])

        affordable_products = {}
        for cost, id in unlocked_products.items():
            if cookie_count >= cost:
                affordable_products[cost] = id

        try:
            # algo-1
            highest_price_affordable_upgrade = max(affordable_products)
            to_purchase_id = affordable_products[highest_price_affordable_upgrade]
            driver.find_element(By.ID, to_purchase_id).click()

            # algo-2
            # highest_price_affordable_upgrade = max(affordable_products)
            # if highest_price_affordable_upgrade == max(unlocked_products):
            #     to_purchase_id = affordable_products[highest_price_affordable_upgrade]
            #     driver.find_element(By.ID, to_purchase_id).click()
        except Exception as e:
            print(e)

        print(f"time left: {int(five_min - time.time())}")

        timeout = time.time() + 5
        if time.time() > five_min:
            break

print("Program ended. Go do something else...")
