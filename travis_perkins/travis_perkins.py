import csv
import os
from datetime import date
import re
import geocoder
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from travis_perkins.constants import USERNAME, PASSWORD
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TravisPerkins(webdriver.Chrome):
    def __init__(self, driver_path='./drivers/chromedriver'):
        self.driver_path = driver_path
        service = Service(executable_path=self.driver_path)
        super(TravisPerkins, self).__init__(service=service)
        self.maximize_window()

    def get_page(self, url):
        self.get(url)

    def close_cookies(self):
        try:
            cookie_btn = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_btn.click()
        except Exception as e:
            pass

    def close_postcode(self):
        try:
            postcode_btn = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test-id="close-button"]'))
            )
            postcode_btn.click()
        except Exception as e:
            pass

    def login_page(self):
        iframe_login = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[data-test-id="oauth-iframe"]'))
        )
        self.switch_to.frame(iframe_login)

        username_input = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_input.clear()
        username_input.send_keys(USERNAME)

        password_input = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_input.clear()
        password_input.send_keys(PASSWORD)

        login_btn = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.ID, "log-in-button"))
        )
        login_btn.click()

    def show_all_products(self):
        while True:
            try:
                show_all_btn = WebDriverWait(self, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test-id="pag-button"]'))
                )
                show_all_btn.click()
            except Exception as e:
                products = []
                product_elements = WebDriverWait(self, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-test-id="product-card"]'))
                )
                for product in product_elements:
                    product_link = product.get_attribute("href")
                    products.append(product_link)

                return products

    def open_length_dropdown(self):
        try:
            dropdown_btn = WebDriverWait(self, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test-id="product-variants"]'))
            )
            dropdown_btn.click()
            return True
        except Exception as e:
            return False


    def get_all_product_lengths(self):
        has_dropdown = self.open_length_dropdown()
        if not has_dropdown:
            return None

        product_lengths = []
        product_length_elements = WebDriverWait(self, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span[data-test-id="list-item-text-wr"]'))
        )
        for item in product_length_elements:
            label = item.text
            product_lengths.append(label)

        return product_lengths

    def click_product_length_by_label(self, label, is_first_label):
        if not is_first_label:
            self.open_length_dropdown()

        xpath = (
            f'//div[@data-test-id="variants-list"]'
            f'//div[@data-test-id="list-item-with-price"]'
            f'[.//span[@data-test-id="list-item-text-wr" and normalize-space()="{label}"]]'
        )
        item = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        item.click()

    def get_product_details(self):
        product_details = {}

        product_specifications = WebDriverWait(self, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="product-specifications"]'))
        )

        product_features = product_specifications.find_elements(By.CSS_SELECTOR, 'div[width="50"]')
        for product_feature in product_features:
            feature = product_feature.find_elements(By.TAG_NAME, 'span')
            product_details[feature[0].text] = feature[1].text

        if 'Pack Quantity' not in product_details:
            product_details['Pack Quantity'] = ''

        if 'Brand Name' not in product_details:
            product_details['Brand Name'] = ''

        return product_details

    def get_location(self):
        myloc = geocoder.ip('me')
        if myloc.ok:
            return myloc.state
        else:
            return ''

    def get_data(self, category, mode):
        product_details = self.get_product_details()
        brand_name = product_details["Brand Name"]
        supplier_sku = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-test-id="product-code"]'))
        ).text
        title = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="product-name"] h1'))
        ).text
        url = self.current_url
        sale_unit = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="main-price"] span'))
        ).text
        pack_qty = product_details["Pack Quantity"]
        if not pack_qty:
            pack_qty_on_title = re.search(r'Pack\s+of\s+(\d+)', title, flags=re.I)
            pack_qty = int(pack_qty_on_title.group(1)) if pack_qty_on_title else None
        pack_uom = "ITEM" if pack_qty else ""
        vat_mode = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="second-price"] span span'))
        ).text
        price_ex_vat = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="second-price"] > span'))
        ).text
        price_inc_vat = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="main-price"] h2'))
        ).text

        unit_price = ''
        unit_basis = ''
        try:
            unit_box = WebDriverWait(self, 0.0001).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="price"] div[class*="TradePriceBlock__UnitPrice"]'))
            )
            unit_price = unit_box.find_element(By.TAG_NAME,"h2").text
            unit_basis = unit_box.find_element(By.CSS_SELECTOR,'span[class*="PerItem"]').text
        except Exception as e:
            pass

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
            'basis': mode,
            'vat_mode': vat_mode.upper().split(".", 1)[0],
            'price_ex_vat': price_ex_vat.split(' ')[0][1:],
            'price_inc_vat': price_inc_vat[1:],
            'display_unit_price_value': unit_price[1:],
            'display_unit_price_basis': unit_basis,
            'currency': price_inc_vat[0],
            'effective_date': date.today().strftime("%d/%m/%Y"),
            'location': self.get_location(),
            'product_details': product_details
        }

        return record


    def write_csv(self, page, mode, record):
        fieldnames = [
            "source_name", "source_type", "component_type", "brand_name", "supplier_sku", "title", "url",
            "sale_unit", "pack_qty", "pack_uom", "basis", "vat_mode", "price_ex_vat", "price_inc_vat",
            "display_unit_price_value", "display_unit_price_basis", "currency", "effective_date", "location",
            "product_details"
        ]

        os.makedirs('./data/travis_perkins', exist_ok=True)
        filename = "./data/travis_perkins/" + page + "_" + mode + "_" + date.today().strftime("%Y%m%d") + ".csv"

        file_exists = os.path.exists(filename)
        file_empty = (not file_exists) or (os.path.getsize(filename) == 0)

        with open(filename, mode="a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header row
            if file_empty:
                writer.writeheader()

            # Write the data rows
            writer.writerows([record])