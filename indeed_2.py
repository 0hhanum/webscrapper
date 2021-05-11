import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f'https://www.indeed.com/jobs?q=python&limit={LIMIT}'


def get_last_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find("ul", {"class": "pagination-list"})
    links = pagination.find_all('a')

    pages = []
    for link in links[:-1]:
        pages.append(int(link.find('span').string))

    max_page = pages[-1]

    return max_page


# indeed 에서 넘어와서. 직종명과 회사명을 추출하는 부분을 따로 빼서 함수로 만든다.

def extract_job(html):
    title = html.find('h2', {'class': 'title'})
    title = title.find('a')['title']  # 직무명.
    company = html.find('span', {'class': 'company'})  # 회사명 찾기.
    company_anchor = company.find('a')

    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company = company.strip()  # 회사명.

    # location 추출하기. sjcl 클래스의 recjobloc 클래스 속에 속성으로 가지고 있다.
    location = html.find('div', {'class': 'recJobLoc'})["data-rc-loc"]

    # 직무, 회사명, 위치까지 모두 가져올 수 있는 함수를 만들었다.
    # indeed 사이트에서 직종을 클릭하면 상세화면, 지원하기 페이지로 넘어가는데 url 을 살펴보면 기존 주소에
    # 직종 id 값이 붙어있는 걸 확인할 수 있다. inspect 로 아이디를 추출해 바로 넘어갈 수 있는 링크를 만들어보자.

    job_id = html['data-jk']
    return {'title': title, 'company': company, 'location': location,
            'link': f'https://www.indeed.com/viewjob?jk={job_id}'}

# 제일 아래에 이걸 한 번에 처리하는 함수를 만들것임.


def get_jobs(last_pages):
    jobs = []
    for page in range(last_pages):
        print(f'Scrapping INDEED: page {page}')
        result = requests.get(f'{URL}&start={page * LIMIT}')
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})

        for result in results:  # 이제 함수로 들어온다.
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_all_jobs():
    last_pages = get_last_pages()
    jobs = get_jobs(last_pages)

    return jobs

# 이렇게 함으로써 main 에서 완전히 깔끔하게 indeed 의 데이터를 얻어올 수 있게되었다.
# stackoverflow 로 이동

