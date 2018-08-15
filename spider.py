import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}


starts_url = 'http://bj.qizuang.com/company/?p='


with open('dianhua.csv', 'a') as f:
    f.write('tel, mob' + '\n')


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


def main(pages):
    start_url = starts_url + str(pages)
    urls = get_company_url(start_url)
    for url in urls:
        company(url)


if __name__ == '__main__':
    for i in range(1, 11):
        main(i)
