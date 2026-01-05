import csv
import os
import re
import time
from datetime import date

import geocoder
from selenium import webdriver
from selenium.common import TimeoutException, ElementClickInterceptedException, NoSuchElementException, \
    StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


def make_driver(headless=False):
    opts = webdriver.ChromeOptions()
    if headless:
        opts.add_argument("--headless=new")

    opts.add_argument("--window-size=1400,900")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--lang=en-GB")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)


def close_cookies(wait):
    try:
        cookie_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(., 'Allow All')]"))
        )
        cookie_btn.click()
    except TimeoutException:
        pass


def close_postcode(wait):
    try:
        close_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test-id="close-button"]'))
        )
        close_btn.click()
    except TimeoutException:
        pass

def show_all_products(driver, wait):
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-test-id="product"]')))
    while True:
        before = len(driver.find_elements(By.CSS_SELECTOR, 'div[data-test-id="product"]'))

        show_more_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[data-test-id="pag-button"]')
        if not show_more_buttons:
            break

        btn = show_more_buttons[0]
        if not btn.is_enabled():
            break

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", btn)

        try:
            wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, 'div[data-test-id="product"]')) > before)
        except Exception as e:
            after = len(driver.find_elements(By.CSS_SELECTOR, 'div[data-test-id="product"]'))
            if after <= before:
                break

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    products = soup.select('[data-test-id="product"]')

    return products


def open_length_dropdown(driver, wait):
    try:
        btn = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test-id="list-placeholder"] div[data-test-id="product-variants"]')))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        driver.execute_script("arguments[0].click();", btn)
        return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="variants-list"]')))
    except TimeoutException:
        return None

def get_all_length_labels(driver, wait, max_scroll=30):
    list_box = open_length_dropdown(driver, wait)
    if list_box is None:
        return None

    labels = []
    seen = set()
    last_count = -1


    for _ in range(max_scroll):
        items = driver.find_elements(By.CSS_SELECTOR, 'div[data-test-id="variants-list"] div[data-test-id="list-item-with-price"]')
        for it in items:
            try:
                lb = it.find_element(By.CSS_SELECTOR, 'span[data-test-id="list-item-text-wr"]').text.strip()
            except Exception as e:
                continue
            if lb and lb not in seen:
                seen.add(lb)
                labels.append(lb)

        if len(labels) == last_count:
            break
        last_count = len(labels)

        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].clientHeight;", list_box)
        time.sleep(0.25)

    driver.execute_script("document.body.click();")

    return labels

def click_length_by_label(driver, wait, label: str):
    list_box = open_length_dropdown(driver, wait)

    xpath = (
        f'//div[@data-test-id="variants-list"]'
        f'//div[@data-test-id="list-item-with-price"]'
        f'[.//span[@data-test-id="list-item-text-wr" and normalize-space()="{label}"]]'
    )
    item = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

    driver.execute_script(
        "arguments[0].scrollTop = arguments[1].offsetTop - arguments[0].clientHeight/2;",
        list_box, item
    )
    time.sleep(0.15)

    driver.execute_script("arguments[0].click();", item)

    try:
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="variants-list"]')))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="product-name"] h1, h1')))
    except TimeoutException:
        driver.execute_script("document.body.click();")


def get_product_detail(soup, key):
    try:
        column_name = soup.find("span", string=lambda s: s and s.strip() == key)
        value = column_name.find_parent("div").find_next_sibling("div").get_text(strip=True)
        return value
    except Exception as e:
        return ""


def get_location():
    myloc = geocoder.ip('me')
    if myloc.ok:
        return myloc.state
    else:
        return ''


def get_data(driver, soup, category, is_login):
    product_detail_soup = soup.find("div", attrs={"data-test-id": "product-specifications"})

    brand_name = get_product_detail(product_detail_soup, "Brand Name")
    supplier_sku = get_product_detail(product_detail_soup, "Manufacturer Model No")
    title = soup.select_one('div[data-test-id="product-name"] h1').get_text(strip=True)
    url = driver.current_url
    sale_unit = soup.find("div", attrs={"data-test-id": "main-price"}).find("span").get_text(strip=True)
    pack_qty = get_product_detail(product_detail_soup, "Pack Quantity")
    if not pack_qty:
        pack_qty_on_title = re.search(r'Pack\s+of\s+(\d+)', title, flags=re.I)
        pack_qty = int(pack_qty_on_title.group(1)) if pack_qty_on_title else None
    pack_uom = "ITEM" if pack_qty else ""
    vat_mode = soup.select_one('div[data-test-id="second-price"] > span > span').get_text(strip=True)
    price_ex_vat = soup.select_one('div[data-test-id="second-price"] > span').find(string=True, recursive=False).strip()
    price_inc_vat = soup.find("div", attrs={"data-test-id": "main-price"}).find("h2").get_text(strip=True)
    unit_box = soup.select_one('div[data-test-id="price"] div[class*="TradePriceBlock__UnitPrice"]')
    unit_price = unit_box.select_one("h2").get_text(strip=True) if unit_box else ''
    unit_basis = unit_box.select_one('span[class*="PerItem"]').get_text(strip=True) if unit_box else ''

    depth = get_product_detail(product_detail_soup, "Depth")
    height = get_product_detail(product_detail_soup, "Height")
    length = get_product_detail(product_detail_soup, "Length")
    weight = get_product_detail(product_detail_soup, "Weight")
    material = get_product_detail(product_detail_soup, "Material")
    colour = get_product_detail(product_detail_soup, "Colour")
    made_to_order = get_product_detail(product_detail_soup, "Made To Order")
    product_details = f"Depth: {depth}, Height: {height}, Length: {length}, Weight: {weight}, Material: {material}, Colour: {colour}, Made To Order: {made_to_order}"

    record = {
        'source_name': 'Travis Perkins',
        'source_type': 'web',
        'component_type': category,
        'brand_name': brand_name,
        'supplier_sku': supplier_sku,
        'title': title,
        'url': url,
        'sale_unit': sale_unit.upper(),
        'pack_qty': pack_qty,
        'pack_uom': pack_uom,
        'basis': 'trade' if is_login else "retail",
        'vat_mode': vat_mode.upper().split(".", 1)[0],
        'price_ex_vat': price_ex_vat[1:],
        'price_inc_vat': price_inc_vat[1:],
        'display_unit_price_value': unit_price[1:],
        'display_unit_price_basis': unit_basis,
        'currency': price_inc_vat[0],
        'effective_date': date.today().strftime("%d/%m/%Y"),
        'location': get_location(),
        'product_details': product_details
    }

    return record


def write_csv(supplier, scope, record):
    fieldnames = ["source_name", "source_type", "component_type", "brand_name", "supplier_sku", "title", "url",
                "sale_unit", "pack_qty", "pack_uom", "basis", "vat_mode", "price_ex_vat", "price_inc_vat",
                "display_unit_price_value", "display_unit_price_basis", "currency", "effective_date", "location", "product_details"
                  ]

    os.makedirs('./data', exist_ok=True)
    filename = "./data/" + supplier + "_" + scope + "_" + date.today().strftime("%Y%m%d") + ".csv"

    file_exists = os.path.exists(filename)
    file_empty = (not file_exists) or (os.path.getsize(filename) == 0)

    with open(filename, mode="a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        if file_empty:
            writer.writeheader()

        # Write the data rows
        writer.writerows([record])



def wait_dom_ready(driver, timeout=30):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") in ("interactive", "complete")
    )

def find_in_any_frame(driver, by, value):
    # default content
    driver.switch_to.default_content()
    els = driver.find_elements(by, value)
    if els:
        return els[0]

    # iframes
    frames = driver.find_elements(By.TAG_NAME, "iframe")
    for f in frames:
        driver.switch_to.default_content()
        driver.switch_to.frame(f)
        els = driver.find_elements(by, value)
        if els:
            return els[0]

    driver.switch_to.default_content()
    return None

def login(wait, email, password, timeout=30):
    driver = wait._driver
    wait_dom_ready(driver, timeout)
    wait = WebDriverWait(
        driver,
        timeout,
        poll_frequency=0.2,
        ignored_exceptions=(NoSuchElementException, StaleElementReferenceException)
    )

    wait.until(lambda d: find_in_any_frame(d, By.ID, "username") is not None)
    wait.until(lambda d: find_in_any_frame(d, By.ID, "password") is not None)

    user_el = find_in_any_frame(driver, By.ID, "username")
    pass_el = find_in_any_frame(driver, By.ID, "password")

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", user_el)
    user_el.clear()
    user_el.send_keys(email)

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", pass_el)
    pass_el.clear()
    pass_el.send_keys(password)

    btn_css = "#log-in-button, form#kc-form-login button[type='submit'], form#kc-form-login input[type='submit'], #kc-login"
    wait.until(lambda d: find_in_any_frame(d, By.CSS_SELECTOR, btn_css) is not None)

    def button_enabled(d):
        btn = find_in_any_frame(d, By.CSS_SELECTOR, btn_css)
        if not btn:
            return False
        disabled_attr = btn.get_attribute("disabled")
        return btn.is_enabled() and (disabled_attr is None)

    wait.until(button_enabled)

    btn = find_in_any_frame(driver, By.CSS_SELECTOR, btn_css)
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)

    try:
        btn.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", btn)

    driver.switch_to.default_content()