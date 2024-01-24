"""Get all Amazon orders and download the invoices"""
import os
import argparse
import json

from selenium import webdriver
from dotenv import load_dotenv

from .navigate import login_to_amazon
from .orders import get_all_order_ids
from .invoices import download_invoice
from .parse import parse_invoice_folder


def main():
    """Get all Amazon orders and download the invoices"""
    parser = argparse.ArgumentParser(description="Download Amazon invoices")
    parser.add_argument("year", type=str, help="The year to download invoices for")
    args = parser.parse_args()

    # Get credentials from environment variables
    load_dotenv()

    try:
        email = os.environ["AMAZON_EMAIL"]
        password = os.environ["AMAZON_PASSWORD"]
    except KeyError:
        print("Please set the AMAZON_EMAIL and AMAZON_PASSWORD environment variables")
        return

    # Set up Selenium WebDriver to show a Firefox window
    driver = webdriver.Firefox()
    try:
        # Log in to Amazon
        driver = login_to_amazon(driver, email, password)

        # Get the order IDs
        order_id_list = get_all_order_ids(driver, year=args.year)

        current_invoices = os.listdir("invoices")

        order_id_list_count = len(order_id_list)

        for idx, order in enumerate(order_id_list):
            if order + ".html" in current_invoices:
                print(
                    f"Skipping invoice {idx+1}/{order_id_list_count} for order {order}"
                )
                continue
            print(
                f"Downloading invoice {idx+1}/{order_id_list_count} for order {order}"
            )
            download_invoice(driver, order, output_folder="invoices")
    finally:
        driver.close()

    orders = parse_invoice_folder("invoices")
    with open("orders.json", "w", encoding="utf-8") as file:
        json.dump(orders, file, indent=4)

    print("Done! Output saved to orders.json")


if __name__ == "__main__":
    main()
