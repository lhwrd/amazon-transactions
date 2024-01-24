"""Functions for getting order IDs from the order history page"""
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def get_order_ids(driver):
    """Get order IDs from the order history page"""
    # Get all the order IDs on the page
    order_ids = driver.find_elements(By.CSS_SELECTOR, ".yohtmlc-order-id")

    # Create a list to store our order IDs
    order_id_list = []

    # Loop through the order IDs
    for order_id in order_ids:
        # Get the text of the order ID
        order_id_text = order_id.text

        if order_id_text.startswith("ORDER #"):
            order_id_text = order_id_text[8:]

        # Add the order ID to our list
        order_id_list.append(order_id_text)

    return order_id_list


def get_all_order_ids(driver, year: str):
    """Get order IDs from the all order history pages"""
    # Navigate to the order history page
    driver.get("https://www.amazon.com/your-orders/orders?timeFilter=year-" + year)

    # Wait for the page to load
    time.sleep(2)

    order_id_list = get_order_ids(driver)

    orders_list_count = len(order_id_list)

    print(f"Found {orders_list_count} orders...")

    # Loop through all of the pages
    while True:
        # Find the next page button
        try:
            next_page_button = driver.find_element(By.CSS_SELECTOR, ".a-last")
        except NoSuchElementException:
            break

        # If the button is disabled, break out of the loop
        if "a-disabled" in next_page_button.get_attribute("class"):
            break

        # Click the next page button
        next_page_button.click()

        # Wait for the page to load
        time.sleep(2)

        next_orders = get_order_ids(driver)
        order_id_list.extend(next_orders)

        if len(order_id_list) == orders_list_count:
            break
        else:
            orders_list_count = len(order_id_list)
            print(f"Found {orders_list_count} orders...")

    print(f"Found {len(order_id_list)} orders in total")

    return order_id_list
