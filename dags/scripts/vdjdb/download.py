from bs4 import BeautifulSoup
import requests

url = 'https://vdjdb.cdr3.net/search'

response = requests.get(url)
if response.status_code != 200:
    print('Error al obtener la pagina: Error '+response.status_code)

content = response.text

soup = BeautifulSoup(content, 'lmxl')
print(soup.prettify())