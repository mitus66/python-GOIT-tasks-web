import asyncio
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any
import aiohttp


class PrivatBankAPIClient:
    BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date={}"  # format: dd.mm.yyyy

    async def fetch_currency_rates(self, session: aiohttp.ClientSession, date: str) -> Dict[str, Any]:
        url = self.BASE_URL.format(date)
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                return self._extract_currency_data(data)
        except aiohttp.ClientError as e:
            print(f"HTTP Error for date {date}: {e}")
            return {date: {}}
        except Exception as e:
            print(f"Unexpected error for date {date}: {e}")
            return {date: {}}

    def _extract_currency_data(self, data: Dict[str, Any]) -> Dict[str, Dict[str, Dict[str, float]]]:
        result = {}
        date = data.get("date")
        if not date:
            return result

        rates = {item['currency']: {'sale': item['saleRate'], 'purchase': item['purchaseRate']}
                 for item in data.get("exchangeRate", [])
                 if item.get('currency') in ['EUR', 'USD'] and 'saleRate' in item and 'purchaseRate' in item}

        if rates:
            result[date] = rates
        return result


class CurrencyRateService:
    def __init__(self, client: PrivatBankAPIClient):
        self.client = client

    async def get_rates_for_last_days(self, days: int) -> List[Dict[str, Any]]:
        today = datetime.today()
        dates = [(today - timedelta(days=i)).strftime("%d.%m.%Y") for i in range(days)]

        async with aiohttp.ClientSession() as session:
            tasks = [self.client.fetch_currency_rates(session, date) for date in dates]
            return await asyncio.gather(*tasks)


def validate_days_argument(arg: str) -> int:
    try:
        days = int(arg)
        if 1 <= days <= 10:
            return days
        else:
            raise ValueError
    except ValueError:
        print("Please provide a number between 1 and 10.")
        sys.exit(1)


async def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <days>")
        sys.exit(1)

    days = validate_days_argument(sys.argv[1])
    client = PrivatBankAPIClient()
    service = CurrencyRateService(client)
    results = await service.get_rates_for_last_days(days)
    print(results)


if __name__ == '__main__':
    asyncio.run(main())

# py .\main.py 4
# [{'26.06.2025': {'EUR': {'sale': 48.7, 'purchase': 47.7}, 'USD': {'sale': 41.8, 'purchase': 41.2}}},
# {'25.06.2025': {'EUR': {'sale': 48.75, 'purchase': 47.75}, 'USD': {'sale': 41.85, 'purchase': 41.2# 5}}},
# {'24.06.2025': {'EUR': {'sale': 48.9, 'purchase': 47.9}, 'USD': {'sale': 42.0, 'purchase': 41.4}}},
# {'23.06.2025': {'EUR': {'sale': 48.6, 'purchase': 47.6}, 'USD': {'sale': 42.05, 'purchase': 41.45}}}]