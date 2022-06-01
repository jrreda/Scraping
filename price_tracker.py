import requests # http requests
from bs4 import BeautifulSoup # web scraping
from send_email import send_email


def get_product_info(url):
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, features="lxml")

    try:
        title = soup.find(id='productTitle').text.strip()
        price = soup.find("span", {"class": "a-price-whole"}).text.encode('ascii','ignore').decode("utf-8").replace('.', '').replace(',', '')
        original_price = soup.select('.a-text-price')[0].text.encode('ascii','ignore').decode("utf-8").split('.')[0] + ' EGP'
    except:
        return None, None, None, None
    
    try:
        soup.select('#availability .a-color-success')[0].get_text().strip()
        available = True
    except:
        available = False

    return title, price, original_price, available



if __name__ == '__main__':
    url = "https://www.amazon.eg/JBL-Waterproof-Bluetooth-Wireless-Speaker/dp/B08MV54YFM/ref=rvi_sccl_9/257-1651775-8068134?pd_rd_w=QWnHb&content-id=amzn1.sym.8f32982e-05a9-49f3-8400-6974214276da&pf_rd_p=8f32982e-05a9-49f3-8400-6974214276da&pf_rd_r=BR1NWZBGZSTG2H36V1EB&pd_rd_wg=mbLYu&pd_rd_r=3e447249-a115-4546-b7f9-21d975b15881&pd_rd_i=B08MV54YFM&psc=1"
    products = [(url, 6500)]
    
    products_below_limit = []
    for product_url, limit in products:
        title, price, original_price, available = get_product_info(product_url)
        print(title, price, original_price, available)
        if (title is not None) and (int(price) < limit) and available:
            products_below_limit.append((url, title, price, original_price))


    if products_below_limit:
        message = "Subject: Price below limit!\n\n"
        message += "Your tracked products are below the given limit!\n\n"
        
        for url, title, price, original_price in products_below_limit:
            message += f"{title}\n"
            message += f"Price: {price}\n"
            message += f"Original Price: {original_price}\n"
            message += f"{url}\n\n"
        
        send_email(message)