import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


ua = UserAgent()

async def get_product_price(url: str) -> float | None:
    headers = {"User-Agent": ua.random}

    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        """ Парсим цену продукта по url """
        try: 
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, "html.parser")

            # Находим цену (Для каждого сайта может быть своя структура)
            price_text = soup.find("meta", property="product:price:amount") 
            if price_text:
                return float(price_text["content"])
            return None
        
        except Exception as err:
            print(f"Ошибка при парсинге {url}: {err}")
            return None
        

        