import requests
from bs4 import BeautifulSoup

URL = f'https://stackoverflow.com/jobs?q=python'


def get_last_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find('div', {'class': 's-pagination'})
    pages = pagination.find_all('span')
    last_page = pages[-2].string
    return int(last_page) // 10


def extract_job(html):
    title = html.find('h2').find('a')['title']
    company, location = html.find('h3').find_all('span', recursive=False)
    # h3 속에는 span 안에 또 span 이 있는 경우가 있다. find_all 로 전부 찾되, 첫 단계의 span 만 탐색. -> recursive
    company, location = company.string.strip(), location.string.strip()  # 언패킹.
    job_id = html['data-jobid']

    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f'https://stackoverflow.com/jobs/{job_id}'
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f'Scrapping SO: page: {page}')
        result = requests.get(f'{URL}&pj={page + 1}')
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', {'class': '-job'})  # class 명으로 찾고있으니 뒷 쪽에 있어도 잘 찾아야함.
        for result in results:  # 이렇게 제일 큰 곳에서 부터 하는 이유가 있음. 한 방에 깊숙히 가도 되는데 너무 느려짐.
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_pages()
    jobs = extract_jobs(last_page)

    return jobs

# 이제 save.py 로 가서 추출한 데이터를 csv 로 옮겨보도록 하자.
