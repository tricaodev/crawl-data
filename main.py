import argparse

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import utils
from selenium.webdriver.support import expected_conditions as EC



BASE_URL = "https://www.travisperkins.co.uk"
COMPONENT_SCOPE = {
    "Concrete Lintel": ["https://www.travisperkins.co.uk/product/building-materials/lintels/concrete-lintels/c/1500069/"],
    "Common Brick": ["https://www.travisperkins.co.uk/product/building-materials/bricks-and-blocks/common-and-concrete-bricks/c/1502019/"],
    "Engineering Brick": ["https://www.travisperkins.co.uk/product/building-materials/bricks-and-blocks/engineering-bricks/c/1500032/"],
    "Facing Bricks": ["https://www.travisperkins.co.uk/product/building-materials/bricks-and-blocks/facing-bricks/c/1500031/"],
    "Steel Lintel": ["https://www.travisperkins.co.uk/product/building-materials/lintels/steel-lintels/c/1500070/"],
    "Concrete Block": [
            "https://www.travisperkins.co.uk/product/building-materials/bricks-and-blocks/blocks/100mm-blocks/c/1500035/",
            "https://www.travisperkins.co.uk/product/building-materials/bricks-and-blocks/blocks/140mm-blocks/c/1500036/",
            "https://www.travisperkins.co.uk/product/building-materials/bricks-and-blocks/blocks/215mm-blocks/c/1591045/",
            "https://www.travisperkins.co.uk/product/building-materials/bricks-and-blocks/blocks/foundation-blocks/c/1591046/"
    ]
}

IS_LOGIN = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default="retail", help='')
    args = parser.parse_args()

    driver = utils.make_driver(headless=False)
    wait = WebDriverWait(driver, 5)

    if args.mode == "trade":
        IS_LOGIN = True
        driver.get("https://www.travisperkins.co.uk/login")

        utils.close_cookies(wait)
        utils.close_postcode(wait)

        utils.login(wait, "hello@fairware.co", "@Bcd1234")


    for category, urls in COMPONENT_SCOPE.items():
        for url in urls:
            driver.get(url)

            # Close cookies banner
            utils.close_cookies(wait)

            # Close postcode banner
            utils.close_postcode(wait)

            # Show all products
            products = utils.show_all_products(driver, wait)

            for product in products:
                product_link = BASE_URL + product.find('a')['href']
                driver.get(product_link)

                # Check if you have dropdown select length
                labels = None
                if category in ["Concrete Lintel", "Steel Lintel"]:
                    labels = utils.get_all_length_labels(driver, wait)

                if labels:
                    for lb in labels:
                        utils.click_length_by_label(driver, wait, lb)

                        html = driver.page_source
                        soup = BeautifulSoup(html, "html.parser")

                        # Get data
                        record = utils.get_data(driver, soup, category, IS_LOGIN)
                        utils.write_csv("travisperkins", args.mode, record)

                else:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="product-name"] h1, h1')))
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")

                    # Get data
                    record = utils.get_data(driver, soup, category, IS_LOGIN)
                    utils.write_csv("travisperkins", args.mode, record)

        print(f"Finished crawling all the data for the {category}")

    driver.quit()