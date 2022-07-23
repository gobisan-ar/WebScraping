import os
import requests
import smtplib
from bs4 import BeautifulSoup

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

BUY_PRICE = 50
PRODUCT_URL = "https://www.amazon.com/_/dp/1098108302?tag=oreilly20-20"

request_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Accept-Language": "en-US,en;q=0.5"
}

response = requests.get(url=PRODUCT_URL, headers=request_headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')

price = soup.find(name="span", id="price").get_text().strip()
reformatted_price = price.split("$")[1].replace(",", '')
price_as_float = float(reformatted_price)

title = soup.find(id="productTitle").get_text().strip().split(",")[0]


if price_as_float < BUY_PRICE:
    message = f"{title} is now {price}"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        result = connection.login(EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{PRODUCT_URL}"
        )
