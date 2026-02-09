import httpx
import json
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


ua = UserAgent()

async def get_product_price(url: str) -> float | None:
    headers = {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    }
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=15.0) as client:
        try:
            response = await client.get(url)
            if response.status_code != 200:
                print(f"DNS Error {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Стратегия для DNS: Ищем блок <script type="application/ld+json">
            scripts = soup.find_all("script", type="application/ld+json")
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    # DNS обычно кладет данные о товаре в список или в объект с типом Product
                    if isinstance(data, list):
                        data = data[0]
                    
                    if data.get("@type") == "Product" or "offers" in data:
                        price = data["offers"].get("price")
                        if price:
                            return float(price)
                except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                    continue

            # Запасной вариант: поиск по классу (у DNS часто это 'product-buy__price')
            price_tag = soup.select_one(".product-buy__price, .price_item-price")
            if price_tag:
                return _clean_price(price_tag.get_text())

            return None
        except Exception as e:
            print(f"DNS Parser Crash: {e}")
            return None

def _clean_price(price_str: str) -> float | None:
    clean_str = re.sub(r'[^\d]', '', price_str)
    return float(clean_str) if clean_str else None

