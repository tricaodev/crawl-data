from travis_perkins.constants import COMPONENT_SCOPE, BASE_URL
from travis_perkins.travis_perkins import TravisPerkins



# crawler = TravisPerkins(driver_path='./drivers/chromedriver.exe') # Driver for Window
crawler = TravisPerkins()

def main(mode):
    crawler.get_page(BASE_URL)
    crawler.close_cookies()
    crawler.close_postcode()

    if mode == "trade":
        crawler.get_page(BASE_URL + "login")
        crawler.login_page()


    for category, urls in COMPONENT_SCOPE.items():
        for url in urls:
            crawler.get_page(url)
            product_links = crawler.show_all_products()

            for link in product_links:
                crawler.get_page(link)

                # Check if you have dropdown select length
                labels = None
                if category in ["Concrete Lintel", "Steel Lintel"]:
                    labels = crawler.get_all_product_lengths()

                if labels:
                    is_first_label = True
                    for label in labels:
                        crawler.click_product_length_by_label(label, is_first_label)
                        is_first_label = False

                        record = crawler.get_data(category, mode)
                        crawler.write_csv("travisperkins", mode, record)

                else:
                    record = crawler.get_data(category, mode)
                    crawler.write_csv("travisperkins", mode, record)

        print(f"Finished crawling all the data for the {category}")