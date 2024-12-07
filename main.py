import requests
from bs4 import BeautifulSoup
import csv

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'referer': 'https://www.zillow.com/homes/Missoula,-MT_rb/'
}

response = requests.get('https://www.zillow.com/portland-or/', headers=header)

properties = []

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    search_results = soup.find(id="grid-search-results")
    if search_results:
        homecards = search_results.find_all("li")
        for card in homecards:
            if card.find("address", {"data-test": "property-card-addr"}):
                more_info = card.find("div", class_="property-card-data")
                info = more_info.find_all("li")
                data = {
                    "address": card.find("address", {"data-test": "property-card-addr"}).text.strip(),
                    "broker": more_info.find("div").text.strip(),
                    "price": card.find("span", {"data-test": "property-card-price"}).text.strip(),
                    "beds": info[0].text.strip(),
                    "bathrooms": info[1].text.strip(),
                    "sqft": info[2].text.strip(),
                    "url": card.find("a", {"data-test": "property-card-link"})["href"]
                }
                properties.append(data)
                print(data)

csv_header = ["Address", "Broker", "Price", "Beds", "Bathrooms", "Square Footage", "URL"]

with open("zillow.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=csv_header)
    writer.writeheader()
    for property in properties:
        writer.writerow({
            "Address": property["address"],
            "Broker": property["broker"],
            "Price": property["price"],
            "Beds": property["beds"],
            "Bathrooms": property["bathrooms"],
            "Square Footage": property["sqft"],
            "URL": property["url"]
        })
