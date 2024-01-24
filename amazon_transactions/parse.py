"""Parse the downloaded html Amazon invoices"""
import os
from bs4 import BeautifulSoup


def find_credit_card_transactions(soup):
    """Find table where "Credit Card transactions" is in a child div"""
    transactions_table = [
        b for b in soup.find_all("b") if "Credit Card transactions" in b.text
    ]

    if not transactions_table:
        return []

    transactions_table = transactions_table[0].parent.parent.parent

    transactions = []
    for transaction in transactions_table.find_all("tr"):
        text = (
            transaction.text.strip().replace("\n", "").replace("\\xa0", "").split(":")
        )

        payment_method = text[0].strip()
        date = text[1].strip()
        amount = text[2].strip()
        transactions.append(
            {"payment_method": payment_method, "date": date, "amount": amount}
        )

    return transactions


def parse_invoice(order_id, invoice_source):
    """Parse the invoice html and return a dictionary of the order"""
    soup = BeautifulSoup(invoice_source, "html.parser")

    # Get the order date
    order_date = soup.find_all("b")[1].parent.text.split("\n")[-2].strip()

    # Get the order total
    order_total = soup.find_all("b")[3].parent.text.split("\n")[-2].strip()

    # Get the items ordered
    items_ordered_table = soup.find_all("table")[-11].find_all("tr")[1:]
    items_ordered = []

    for item_ordered in items_ordered_table:
        tds = item_ordered.find_all("td")
        item = tds[0].text.split("\n\n    ")
        quantity = item[0].replace("\n", "").strip()
        if len(item) < 2:
            continue
        item = item[2]
        price = tds[1].text.strip()

        items_ordered.append([item, quantity, price])

    transactions = find_credit_card_transactions(soup)

    order = {
        "order_id": order_id,
        "order_date": order_date,
        "order_total": order_total,
        "items_ordered": items_ordered,
        "transactions": transactions,
    }

    return order


def parse_invoice_folder(invoices_folder):
    """Parse all invoices in a folder and return a list of orders"""
    invoices = os.listdir(invoices_folder)
    orders = []
    for invoice in invoices:
        with open(invoices_folder + "/" + invoice, encoding="utf-8") as file:
            order_id = invoice.split(".")[0]
            order = parse_invoice(order_id, file.read())

            orders.append(order)
    return orders
