import requests
import html5lib
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def index(request):
    URL = 'https://www.amazon.it/s?k=ps4'
    if request.method =='POST':
        URL = request.POST.get('url')
        print(f"Url-Call: {URL}")

    headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html5lib')
    prod_list = []
    products_list = soup.find('div', class_='s-main-slot s-result-list s-search-results sg-row').find_all('div', recursive=False)
    for child in products_list:
        data_asin = child.get('data-asin')
        product_price = child.find('span', class_='a-price-whole')
        product_link = child.find('a', class_='a-size-base a-link-normal a-text-normal')
        product_name = child.find('span', class_='a-size-base-plus a-color-base a-text-normal')
        product_img = child.find('img', class_='s-image')
        # print(product_img)
        if data_asin and product_price and product_link and product_name is not None:
            prod_list.append({'name': product_name.text, 'price': product_price.text, 'asin': data_asin,\
                              'src': product_img.get('src'), 'link': product_link.get('href')})

    print(len(prod_list))

    data = {'list_items': prod_list}
    return render(request, 'index.html', context=data)




