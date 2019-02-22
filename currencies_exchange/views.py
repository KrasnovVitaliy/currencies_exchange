from aiohttp import web
import aiohttp_jinja2
import logging
import db

logger = logging.getLogger(__name__)


class IndexView(web.View):
    @aiohttp_jinja2.template('index.html')
    async def get(self):
        objs = db.session.query(db.CurrenciesRecord).order_by("id desc").limit(20)
        data = [obj.to_json() for obj in objs]

        usd_raif_buy_currencies = []
        usd_raif_sale_currencies = []
        eur_raif_buy_currencies = []
        eur_raif_sale_currencies = []
        usd_best_buy_currencies = []
        usd_best_sale_currencies = []
        eur_best_buy_currencies = []
        eur_best_sale_currencies = []
        dates = []
        for item in data:
            if item['code'] == 'USD':
                usd_raif_buy_currencies.append(item['raif_buy'])
                usd_best_buy_currencies.append(item['best_buy'])
                usd_raif_sale_currencies.append(item['raif_sale'])
                usd_best_sale_currencies.append(item['best_sale'])
                dates.append(item['create_date'])
            if item['code'] == 'EUR':
                eur_raif_buy_currencies.append(item['raif_buy'])
                eur_best_buy_currencies.append(item['best_buy'])
                eur_raif_sale_currencies.append(item['raif_sale'])
                eur_best_sale_currencies.append(item['best_sale'])
        return {
            'last_currencies': data[:2],
            'old_currencies': data[2:],
            'usd_raif_buy_currencies': usd_raif_buy_currencies,
            'usd_best_buy_currencies': usd_best_buy_currencies,
            'usd_raif_sale_currencies': usd_raif_sale_currencies,
            'usd_best_sale_currencies': usd_best_sale_currencies,
            'eur_raif_buy_currencies': eur_raif_buy_currencies,
            'eur_best_buy_currencies': eur_best_buy_currencies,
            'eur_raif_sale_currencies': eur_raif_sale_currencies,
            'eur_best_sale_currencies': eur_best_sale_currencies,
            'dates': dates,
        }
