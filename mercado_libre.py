import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

class Scraper():
    def __init__(self):
        self.base_url = 'https://listado.mercadolibre.com.pe/'

    def scraping(self, product_name):
        cleaned_name = product_name.replace(" ", "-").lower()
        urls = [self.base_url + cleaned_name]

        page_number = 50
        for i in range(0, 10000, 50):
            urls.append(f"{self.base_url}{cleaned_name}_Desde_{page_number + 1}_NoIndex_True")
            page_number += 50

        self.data = []
        c = 1
            
        for i, url in enumerate(urls, start=1):

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
                
            content = soup.find_all('li', class_='ui-search-layout__item')
            
            if not content:
                print("\nTermino el scraping.")
                break

            print(f"\nScrapeando página numero {i}. {url}")
            
            
            for post in content:
                title = post.find('h3', class_='ui-search-item__title').text
                price = post.find('span', class_='andes-money-amount__fraction').text
                post_link = post.find("a")["href"]
                try:
                    img_link = post.find("img")["data-src"]
                except:
                    img_link = post.find("img")["src"]
                
                post_data = {
                    "title": title.strip(),
                    "price": price.strip(),
                    "post link": post_link.strip(),
                    "image link": img_link.strip()            
                }
                self.data.append(post_data)
                c += 1

        return self.data

@app.route('/mercadoLibre/<string:product_name>', methods=['GET'])
def mercadoLibre(product_name):
    s = Scraper()
    s.scraping(product_name)
    return jsonify({"datos": s.data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
