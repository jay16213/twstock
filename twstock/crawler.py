import datetime
from urllib.parse import urljoin
from pathlib import Path
import requests
from twstock import stock

# example fetch url
# https://www.twse.com.tw/exchangeReport/MI_INDEX?response=html&date=20200327&type=ALL
class MyFetcher(stock.BaseFetcher):
    REPORT_URL = urljoin(stock.TWSE_BASE_URL, 'exchangeReport/MI_INDEX')

    def fetch_daily(self, response_type: str='html', type: str='ALL'):
        current_date = datetime.date.today()
        params = {'response': response_type, 'date': current_date.strftime('%Y%m%d'), 'type': type}

        for _ in range(5):
            try:
                r = requests.get(self.REPORT_URL, params=params)
            except requests.exceptions.RequestException as e:
                print("Get {url} failed: {error}".format(self.REPORT_URL, e))
                continue
            else:
                data = r.content
                break

        if data != '':
            try:
                save_path = current_date.strftime('%Y%m')
                print(save_path)
                if not Path(save_path).exists():
                    Path(save_path).mkdir(parents=True,exist_ok=True)
                with open('{}/DailyReport_{}.html'.format(save_path, current_date.strftime('%Y%m%d')), 'wb') as f:
                    f.write(data)
            except EnvironmentError as e:
                print(e)

if __name__ == "__main__":
    fetcher = MyFetcher()
    fetcher.fetch_daily()
