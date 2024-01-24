"""Download an invoice from Amazon.com"""
import time
import re
from selenium import webdriver


def download_invoice(driver: webdriver.Firefox, order_id: str, output_folder: str):
    """Download an invoice from Amazon.com"""
    # Throw an error if the order ID is invalid
    if not re.match(r"\d{3}-\d{7}-\d{7}", order_id):
        raise ValueError("Invalid order ID")

    # Go to the order page
    driver.get(
        "https://www.amazon.com/gp/css/summary/print.html/ref=od_aui_print_invoice?ie=UTF8&orderID="
        + order_id
    )

    # Wait for the page to load
    time.sleep(2)

    # Get the page source
    page_source = driver.page_source

    output_path = f"{output_folder}/{order_id}.html"

    # Download the page source
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(page_source)
