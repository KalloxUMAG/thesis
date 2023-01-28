import requests
from lxml import html

url = 'http://opig.stats.ox.ac.uk/webapps/covabdab/'


def get_file(url, name, extension):
    response = requests.get(url)
    if response.status_code == 200:
        print('url descargada')
        save_file(name, response.content, extension)
    else:
        print('No se pudo obtener los datos correspondiente a la url ' + url)


def save_file(name, content, extension):
    file = open('./dags/files/covabdab/downloads/'+name+'.'+extension, 'wb')
    file.write(content)
    file.close()


def download():
    page = requests.get(url)
    tree = html.fromstring(page.content)
    date = str(tree.xpath('/html/body/div[2]/div/div[2]/div/p/text()[7]'))
    date = date[date.find(':')+2:date.find(')')]
    print(date)

    file_url = str(tree.xpath('//*[@id="collapseOne"]/div/a[1]/@href'))
    file_url = file_url[2:-2].split('/')[5]

    download_url = url + 'static/downloads/' + file_url
    print(download_url)
    get_file(download_url, 'CoV-AbDab', 'csv')


if __name__ == '__main__':
    download()
