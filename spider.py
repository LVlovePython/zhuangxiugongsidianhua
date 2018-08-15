import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}


city_url = 'http://www.qizuang.com/city/'

with open('dianhua.csv', 'a') as f:
    f.write('tel, mob' + '\n')


def choose_city(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    cities = soup.select('.span1 li')
    urls = soup.select('.span1 a')
    datas = []
    for city, url in zip(cities, urls):
        data = {
            'city': city.text,
            'url': url.get('href')
        }
        datas.append(data)
    return datas


def get_company_url(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    company_url = soup.select('.company_tituw > a')
    urls = []
    for each_url in company_url:
        url = each_url.get('href')
        urls.append(url)
        print(url)
    return urls


def company(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    tels = soup.select('.tel')
    mobs = soup.select('.mob')
    for tel, mob in zip(tels, mobs):
        data = {
            'tel': tel.text,
            'mob': mob.text
        }
        print(data)
        save_to_file(data)


def save_to_file(data):
    with open('dianhua.csv', 'a') as f:
        f.write(data['tel'] + ',' + data['mob'] + '\n')


def main():
    data = choose_city(city_url)
    keyword = input('请选择你想的城市：')
    for i in data:
        if keyword == i['city']:
            starts_url = i['url']
        else:
            None
    pages = int(input('请输入你想爬取的页数：'))
    for page in range(1, pages + 1):
        start_url = starts_url + 'company/?p=' + str(page)
        urls = get_company_url(start_url)
        for url in urls:
            company(url)


if __name__ == '__main__':
    main()
