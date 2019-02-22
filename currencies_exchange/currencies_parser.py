from bs4 import BeautifulSoup
import requests
import db

RAIFEISSEN_URL = "https://www.raiffeisen.ru/currency_rates/"
RAIFESSEN_CURRENCIES_ROW_ALLOCATOR = "b-table__row"
RAIFESSEN_CURRENCIES_TABLE_ALLOCATOR = "b-table-currency"

BANKI_URL = "https://www.banki.ru/products/currency/cash/kazan~/"
BANKI_CURRENCIES_TABLE_ALLOCATOR = "currency-table__table"
BANKI_CURRENCIES_ROW_ALLOCATOR = "currency-table__bordered-row"


def parse_raifessen_page() -> list:
    rsp = requests.get(RAIFEISSEN_URL)
    soup = BeautifulSoup(rsp.text)

    currencies_table = soup.find("div", {"class": RAIFESSEN_CURRENCIES_TABLE_ALLOCATOR})
    currencies_rows = currencies_table.findAll("div", {"class": RAIFESSEN_CURRENCIES_ROW_ALLOCATOR})

    currencies_exchanges = []
    for row in currencies_rows:
        children = row.findChildren("div", recursive=False)
        child_num = 0
        currencies_exchange = {}
        for child in children:
            if child_num == 0:
                currencies_exchange['code'] = child.text.strip()
            if child_num == 2:
                currencies_exchange['name'] = child.text.strip()
            if child_num == 3:
                currencies_exchange['buy'] = child.text.strip().replace(',', '.')
            if child_num == 4:
                currencies_exchange['sale'] = child.text.strip().replace(',', '.')
            child_num += 1
        currencies_exchanges.append(currencies_exchange)
    return currencies_exchanges


def parse_banki_page() -> list:
    rsp = requests.get(BANKI_URL)
    soup = BeautifulSoup(rsp.text)

    currencies_table = soup.find("table", {"class": BANKI_CURRENCIES_TABLE_ALLOCATOR})
    currencies_rows = currencies_table.findAll("tr", {"class": BANKI_CURRENCIES_ROW_ALLOCATOR})

    currencies_exchanges = []
    for row in currencies_rows:
        children = row.findChildren("td", recursive=False)
        child_num = 0
        currencies_exchange = {}
        for child in children:
            if child_num == 0:
                currencies_exchange['code'] = child.text.strip()
            if child_num == 1:
                currencies_exchange['cb'] = child.findChild().text.strip().replace(',', '.')
            if child_num == 2:
                currencies_exchange['buy'] = child.findChildren()[1].text.strip().replace(',', '.')
                currencies_exchange['best_buy'] = child.findChildren()[2].text.strip().replace('\n', '').replace('\t',
                                                                                                                 '')
            if child_num == 3:
                currencies_exchange['sale'] = child.findChildren()[1].text.strip().replace(',', '.')
                currencies_exchange['best_sale'] = child.findChildren()[2].text.strip().replace('\n', '').replace('\t',
                                                                                                                  '')
            child_num += 1
        currencies_exchanges.append(currencies_exchange)
    return currencies_exchanges


def save_data_to_db(raifessen_currency_exchanges, banki_currency_exchanges):
    for banki_item in banki_currency_exchanges:
        for raifessen_item in raifessen_currency_exchanges:
            if banki_item['code'] == raifessen_item['code']:
                obj = db.CurrenciesRecord(
                    code=banki_item['code'], name=raifessen_item['name'], cb_currency=float(banki_item['cb']),
                    raif_buy=float(raifessen_item['buy']), raif_sale=float(raifessen_item['sale']),
                    best_buy=float(banki_item['buy']), best_sale=float(banki_item['sale']),
                    best_buyer=banki_item['best_buy'], best_sailer=banki_item['best_sale'])
                db.session.add(obj)
                db.session.commit()


def get_currencies():
    raifessen_currency_exchanges = parse_raifessen_page()
    banki_currency_exchanges = parse_banki_page()

    save_data_to_db(raifessen_currency_exchanges, banki_currency_exchanges)
